"""
CLI result decoder for cross-referenced values.
"""

from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)


class CLIResultDecoder:
    """Universal decoder that works with both sync and async clients."""
    
    def __init__(self, client):
        """Initialize decoder with API client (sync or async)."""
        self.client = client
        self.api_def = client.api_definition
        self._lookup_cache = {}
        self._is_async = hasattr(client, '__aenter__')  # Detect async client
        
    def decode_result(self, method_name: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """Decode a method result by resolving cross-referenced values."""
        if result.get("status") != "success":
            return result
            
        # Get method definition
        method_def = self.api_def.get("operations", {}).get(method_name)
        if not method_def:
            return result
            
        # Get linkages from API definition (generated automatically)
        set_methods = method_def.get("_decoder_set_methods", [])
        
        if set_methods:
            # Find the main data key (not 'status')
            data_keys = [k for k in result.keys() if k != "status"]
            if len(data_keys) == 1:
                data_key = data_keys[0]
                data = result[data_key]
                
                # If it's a list, try to decode each item
                if isinstance(data, list) and data:
                    decoded_items = []
                    for item in data:
                        if isinstance(item, dict):
                            # Try each set method to find applicable cross-references
                            decoded = item.copy()
                            for set_method in set_methods:
                                decoded = self._decode_item(decoded, set_method)
                            decoded_items.append(decoded)
                        else:
                            decoded_items.append(item)
                    result[data_key] = decoded_items
                    
        elif method_name.startswith("get") and len(result) > 1:
            # Generic fallback for other get methods
            data_keys = [k for k in result.keys() if k != "status"]
            if len(data_keys) == 1:
                data_key = data_keys[0]
                data = result[data_key]
                
                # If it's a list, try to decode each item
                if isinstance(data, list) and data:
                    # Try to find corresponding set method
                    potential_set_method = method_name.replace("get", "set")
                    if potential_set_method in self.api_def.get("operations", {}):
                        decoded_items = []
                        for item in data:
                            if isinstance(item, dict):
                                decoded = self._decode_item(item, potential_set_method)
                                decoded_items.append(decoded)
                            else:
                                decoded_items.append(item)
                        result[data_key] = decoded_items
                        
        return result
    
    async def decode_result_async(self, method_name: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """Async version with parallel lookup calls for better performance."""
        import time
        start_time = time.time()
        
        if result.get("status") != "success":
            return result
            
        # Get method definition
        method_def = self.api_def.get("operations", {}).get(method_name)
        if not method_def:
            return result
            
        # Get linkages from API definition (generated automatically)
        set_methods = method_def.get("_decoder_set_methods", [])
        
        if set_methods:
            # Find the main data key (not 'status')
            data_keys = [k for k in result.keys() if k != "status"]
            if len(data_keys) == 1:
                data_key = data_keys[0]
                data = result[data_key]
                
                # If it's a list, try to decode each item
                if isinstance(data, list) and data:
                    # Collect all unique lookup methods needed across all items and methods
                    all_lookup_methods = set()
                    for item in data:
                        if isinstance(item, dict):
                            for set_method in set_methods:
                                lookup_methods = self._get_required_lookup_methods(item, set_method)
                                all_lookup_methods.update(lookup_methods)
                    
                    # Execute all unique lookups in parallel (only uncached ones)
                    uncached_methods = [m for m in all_lookup_methods if m not in self._lookup_cache]
                    if uncached_methods:
                        import asyncio
                        lookup_start = time.time()
                        logger.debug(f"Calling {len(uncached_methods)} lookup methods: {uncached_methods}")
                        lookup_results = await asyncio.gather(
                            *[self._get_lookup_values_async(method) for method in uncached_methods],
                            return_exceptions=True
                        )
                        lookup_end = time.time()
                        logger.debug(f"Lookup calls took {lookup_end - lookup_start:.2f} seconds")
                        
                        # Build lookup cache from results
                        for method_name_lookup, lookup_values in zip(uncached_methods, lookup_results):
                            if isinstance(lookup_values, dict):
                                self._lookup_cache[method_name_lookup] = lookup_values
                    else:
                        logger.debug("All lookup methods already cached")
                    
                    # Now decode all items using the cached lookups
                    decoded_items = []
                    for item in data:
                        if isinstance(item, dict):
                            decoded = item.copy()
                            for set_method in set_methods:
                                decoded = self._decode_item_with_cache(decoded, set_method)
                            decoded_items.append(decoded)
                        else:
                            decoded_items.append(item)
                    result[data_key] = decoded_items
                    
        elif method_name.startswith("get") and len(result) > 1:
            # Generic fallback for other get methods
            data_keys = [k for k in result.keys() if k != "status"]
            if len(data_keys) == 1:
                data_key = data_keys[0]
                data = result[data_key]
                
                # If it's a list, try to decode each item
                if isinstance(data, list) and data:
                    # Try to find corresponding set method
                    potential_set_method = method_name.replace("get", "set")
                    if potential_set_method in self.api_def.get("operations", {}):
                        # Collect all unique lookup methods needed
                        all_lookup_methods = set()
                        for item in data:
                            if isinstance(item, dict):
                                lookup_methods = self._get_required_lookup_methods(item, potential_set_method)
                                all_lookup_methods.update(lookup_methods)
                        
                        # Execute all unique lookups in parallel (only uncached ones)
                        uncached_methods = [m for m in all_lookup_methods if m not in self._lookup_cache]
                        if uncached_methods:
                            import asyncio
                            logger.debug(f"Calling {len(uncached_methods)} lookup methods: {uncached_methods}")
                            lookup_results = await asyncio.gather(
                                *[self._get_lookup_values_async(method) for method in uncached_methods],
                                return_exceptions=True
                            )
                            
                            # Build lookup cache from results
                            for method_name_lookup, lookup_values in zip(uncached_methods, lookup_results):
                                if isinstance(lookup_values, dict):
                                    self._lookup_cache[method_name_lookup] = lookup_values
                        else:
                            logger.debug("All lookup methods already cached")
                        
                        # Now decode all items using the cached lookups
                        decoded_items = []
                        for item in data:
                            if isinstance(item, dict):
                                decoded = self._decode_item_with_cache(item, potential_set_method)
                                decoded_items.append(decoded)
                            else:
                                decoded_items.append(item)
                        result[data_key] = decoded_items
        
        end_time = time.time()
        logger.debug(f"Decoder took {end_time - start_time:.2f} seconds")
        return result
        
    def _decode_item(self, item: Dict[str, Any], reference_method: str) -> Dict[str, Any]:
        """Decode an individual item using a reference method's parameters."""
        method_def = self.api_def.get("operations", {}).get(reference_method)
        if not method_def:
            return item
            
        decoded = item.copy()
        params = method_def.get("parameters", {})
        
        for field_name, field_value in item.items():
            if field_name in params:
                param_def = params[field_name]
                
                # Check if this parameter has a values_from reference
                values_from = param_def.get("_values_from") or param_def.get("values_from")
                if values_from and field_value is not None:
                    # Get lookup values
                    lookup_values = self._get_lookup_values(values_from)
                    if lookup_values:
                        # Convert field value to string for lookup
                        str_value = str(field_value)
                        if str_value in lookup_values:
                            # Add decoded value as a new field
                            decoded[f"{field_name}_decoded"] = lookup_values[str_value]
                            
        return decoded
    
    def _get_required_lookup_methods(self, item: Dict[str, Any], reference_method: str) -> set:
        """Get all lookup methods needed for an item using a reference method."""
        method_def = self.api_def.get("operations", {}).get(reference_method)
        if not method_def:
            return set()
            
        lookup_methods = set()
        params = method_def.get("parameters", {})
        
        for field_name, field_value in item.items():
            if field_name in params:
                param_def = params[field_name]
                values_from = param_def.get("_values_from") or param_def.get("values_from")
                if values_from and field_value is not None:
                    lookup_methods.add(values_from)
                    
        return lookup_methods
    
    def _decode_item_with_cache(self, item: Dict[str, Any], reference_method: str) -> Dict[str, Any]:
        """Decode an item using pre-cached lookup values."""
        method_def = self.api_def.get("operations", {}).get(reference_method)
        if not method_def:
            return item
            
        decoded = item.copy()
        params = method_def.get("parameters", {})
        
        for field_name, field_value in item.items():
            if field_name in params:
                param_def = params[field_name]
                values_from = param_def.get("_values_from") or param_def.get("values_from")
                if values_from and field_value is not None:
                    # Use cached lookup values
                    lookup_values = self._lookup_cache.get(values_from)
                    if lookup_values:
                        str_value = str(field_value)
                        if str_value in lookup_values:
                            decoded[f"{field_name}_decoded"] = lookup_values[str_value]
                            
        return decoded
        
    def _get_lookup_values(self, method_name: str) -> Optional[Dict[str, str]]:
        """Get lookup values from a values_from method."""
        if method_name in self._lookup_cache:
            return self._lookup_cache[method_name]
            
        # Check if method exists and can be called without parameters
        method_def = self.api_def.get("operations", {}).get(method_name)
        if not method_def:
            return None
            
        # Check if method requires parameters
        required_params = [
            name for name, info in method_def.get("parameters", {}).items()
            if info.get("required", False)
        ]
        
        if required_params:
            # Can't call methods that require parameters
            return None
            
        try:
            # Call the method
            method = getattr(self.client, method_name, None)
            if not method:
                return None
                
            result = method()
            
            if result.get("status") == "success":
                # Extract values - need to handle different response formats
                values = self._extract_lookup_values(result)
                self._lookup_cache[method_name] = values
                return values
                
        except Exception as e:
            logger.debug(f"Error calling {method_name} for lookups: {e}")
            
        return None
        
    def _extract_lookup_values(self, result: Dict[str, Any]) -> Dict[str, str]:
        """Extract value/description pairs from a lookup method result."""
        values = {}
        
        # Find the data key (not 'status')
        for key, data in result.items():
            if key == "status":
                continue
                
            if isinstance(data, list) and data and isinstance(data[0], dict):
                # Standard format with value/description
                if "value" in data[0] and "description" in data[0]:
                    for item in data:
                        values[str(item["value"])] = item["description"]
                    break
                # Format with code/name
                elif "code" in data[0] and "name" in data[0]:
                    for item in data:
                        values[str(item["code"])] = item["name"]
                    break
                # Format with id/description
                elif "id" in data[0] and "description" in data[0]:
                    for item in data:
                        values[str(item["id"])] = item["description"]
                    break
                # Format with other common patterns
                elif len(data[0]) == 2:
                    # Try to guess key/value pairs
                    keys = list(data[0].keys())
                    if any(k in ["value", "code", "id", "key"] for k in keys):
                        value_key = next(k for k in keys if k in ["value", "code", "id", "key"])
                        desc_key = next(k for k in keys if k != value_key)
                        for item in data:
                            values[str(item[value_key])] = str(item[desc_key])
                        break
                        
        return values


    async def _get_lookup_values_async(self, method_name: str) -> Optional[Dict[str, str]]:
        """Async version of lookup values retrieval with caching."""
        if method_name in self._lookup_cache:
            return self._lookup_cache[method_name]
            
        # Check if method exists and can be called without parameters
        method_def = self.api_def.get("operations", {}).get(method_name)
        if not method_def:
            return None
            
        # Check if method requires parameters
        required_params = [
            name for name, info in method_def.get("parameters", {}).items()
            if info.get("required", False)
        ]
        
        if required_params:
            # Can't call methods that require parameters
            return None
            
        try:
            # Call the method
            method = getattr(self.client, method_name, None)
            if not method:
                return None
                
            result = await method()
            
            if result.get("status") == "success":
                # Extract values - need to handle different response formats
                values = self._extract_lookup_values(result)
                self._lookup_cache[method_name] = values
                return values
                
        except Exception as e:
            logger.debug(f"Error calling {method_name} for lookups: {e}")
            
        return None


# Aliases for backward compatibility
SyncCLIResultDecoder = CLIResultDecoder
AsyncCLIResultDecoder = CLIResultDecoder