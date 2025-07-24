#!/usr/bin/env uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "httpx>=0.24.0",
#     "pydantic>=2.0.0",
#     "python-dotenv>=1.0.0",
#     "tenacity>=8.2.0",
# ]
# ///
"""
VoIP.ms Call Recordings Inspector and Downloader

This script:
1. Lists all call recordings for your account
2. Fetches CDR (Call Detail Records) to compare metadata
3. Downloads recording files locally
4. Shows the relationship between CDR and recording data

Output:
- recordings/ directory with audio files
- call_recordings_report.json with all metadata

Usage:
    uv run inspect_call_recordings.py
    uv run inspect_call_recordings.py --days 30
    uv run inspect_call_recordings.py --download  # Actually download audio files
"""

import asyncio
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List

import httpx

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from voipms import VoIPMSAsyncClient, VoIPMSError


class CallRecordingsInspector:
    """Inspect and download call recordings with metadata analysis"""

    def __init__(self, client: VoIPMSAsyncClient, download_audio: bool = False):
        self.client = client
        self.download_audio = download_audio
        self.recordings_dir = Path("recordings")
        self.report = {
            "inspection_date": datetime.now().isoformat(),
            "accounts": {},
            "recordings": {},
            "cdr_records": {},
            "analysis": {},
        }

    async def inspect_all(self, days: int = 90) -> Dict[str, Any]:
        """Run complete inspection"""
        print("VoIP.ms Call Recordings Inspector")
        print("=" * 50)

        # Step 1: Get all call accounts
        print("\n1. Getting call accounts...")
        accounts = await self._get_call_accounts()
        if not accounts:
            print("   ❌ No call accounts found")
            return self.report

        # Step 2: Get recordings for each account
        print(f"\n2. Getting recordings for {len(accounts)} accounts...")
        all_recordings = await self._get_all_recordings(accounts, days)

        # Step 3: Get CDR only for dates with recordings
        print("\n3. Getting CDR for recorded call dates...")
        cdr_records = await self._get_cdr_for_recordings(all_recordings)

        # Step 4: Analyze and compare data
        print("\n4. Analyzing recording vs CDR data...")
        await self._analyze_recordings_vs_cdr(all_recordings, cdr_records)

        # Step 5: Download recordings if requested
        if self.download_audio and all_recordings:
            print(f"\n5. Downloading {len(all_recordings)} recording files...")
            await self._download_recordings(all_recordings)

        # Save report
        report_file = "call_recordings_report.json"
        with open(report_file, "w") as f:
            json.dump(self.report, f, indent=2, sort_keys=True)

        print(f"\n✅ Report saved to: {report_file}")

        return self.report

    async def _get_call_accounts(self) -> List[str]:
        """Get all call accounts"""
        try:
            result = await self.client.getCallAccounts()
            if result.get("status") == "success" and "accounts" in result:
                accounts = [acc["value"] for acc in result["accounts"] if acc["value"] != "all"]
                self.report["accounts"] = result["accounts"]
                print(f"   ✓ Found {len(accounts)} accounts: {', '.join(accounts)}")
                return accounts
        except VoIPMSError as e:
            print(f"   ✗ Error getting accounts: {e}")
        return []

    async def _get_all_recordings(
        self, accounts: List[str], days: int = 90
    ) -> List[Dict[str, Any]]:
        """Get recordings for all accounts"""
        all_recordings = []

        # Calculate date range
        to_date = datetime.now()
        from_date = to_date - timedelta(days=days)
        date_params = {
            "date_from": from_date.strftime("%Y-%m-%d"),
            "date_to": to_date.strftime("%Y-%m-%d"),
        }

        for account in accounts:
            print(f"   Checking account {account}...", end="", flush=True)
            try:
                # Get recordings list for this account
                result = await self.client.getCallRecordings(account=account, **date_params)

                if result.get("status") == "success" and "recordings" in result:
                    recordings = result["recordings"]
                    print(f" found {len(recordings)} recordings")

                    # Get detailed info for each recording
                    for rec in recordings:
                        recording_id = rec.get("callrecording", rec.get("recording", rec.get("id")))
                        if recording_id:
                            # For now, just use the listing data without fetching details
                            # The getCallRecording method might not exist or work as expected
                            full_info = {**rec}
                            full_info["account"] = account
                            all_recordings.append(full_info)
                            self.report["recordings"][recording_id] = full_info
                        else:
                            print(f"\n     WARNING: No recording ID found in {rec}")
                else:
                    print(" no recordings")

            except VoIPMSError as e:
                print(f" error: {e.code}")

        print(f"\n   Total recordings found: {len(all_recordings)}")
        return all_recordings

    async def _get_cdr_for_recordings(
        self, recordings: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Get CDR records only for dates that have recordings"""
        if not recordings:
            return []

        # Get unique dates from recordings
        recording_dates = set()
        for rec in recordings:
            if rec.get("datetime"):
                # Extract date from datetime like "2025-07-17 10:13:08"
                date_part = rec["datetime"].split()[0]
                recording_dates.add(date_part)

        if not recording_dates:
            return []

        print(f"   Getting CDR for {len(recording_dates)} dates with recordings...")
        all_cdr = []

        for date_str in sorted(recording_dates):
            try:
                # Get CDR with all call statuses
                result = await self.client.getCDR(
                    date_from=date_str,
                    date_to=date_str,
                    answered="1",  # Need to pass "1" not True for these parameters
                    noanswer="1",
                    busy="1", 
                    failed="1",
                    # timezone="-5" gets added automatically as smart default
                )

                if result.get("status") == "success" and "cdr" in result:
                    date_cdr = result["cdr"]
                    all_cdr.extend(date_cdr)
                    print(f"     {date_str}: {len(date_cdr)} CDR records")

                    # Store CDR records for matching
                    for cdr in date_cdr:
                        if cdr.get("uniqueid"):
                            self.report["cdr_records"][cdr["uniqueid"]] = cdr
                        # Also index by caller+destination+time for matching
                        caller = (
                            cdr.get("callerid", "").replace('"', "").split("<")[-1].replace(">", "")
                            if cdr.get("callerid")
                            else ""
                        )
                        key = f"{cdr.get('date')}_{caller}_{cdr.get('destination')}"
                        self.report["cdr_records"][key] = cdr

            except Exception as e:
                print(f"     {date_str}: Error - {e}")

        print(f"   ✓ Found {len(all_cdr)} total CDR records for recording dates")
        return all_cdr

    async def _analyze_recordings_vs_cdr(self, recordings: List[Dict], cdr_records: List[Dict]):
        """Compare recording data with CDR data"""
        matched = 0
        unmatched_recordings = []
        recordings_with_cdr = []

        # Try to match recordings with CDR
        for rec in recordings:
            # Try different matching strategies
            cdr_match = None

            # Strategy 1: Match by uniqueid if available
            if rec.get("uniqueid"):
                cdr_match = next(
                    (c for c in cdr_records if c.get("uniqueid") == rec["uniqueid"]), None
                )

            # Strategy 2: Match by timestamp and phone numbers
            if not cdr_match and rec.get("date"):
                rec_date = rec["date"]
                rec_caller = rec.get("callerid", rec.get("caller", ""))
                rec_dest = rec.get("destination", rec.get("called", ""))

                cdr_match = next(
                    (
                        c
                        for c in cdr_records
                        if c.get("date") == rec_date
                        and (c.get("callerid") == rec_caller or c.get("destination") == rec_dest)
                    ),
                    None,
                )

            if cdr_match:
                matched += 1
                recordings_with_cdr.append(
                    {
                        "recording": rec,
                        "cdr": cdr_match,
                        "comparison": self._compare_fields(rec, cdr_match),
                    }
                )
            else:
                unmatched_recordings.append(rec)

        # Analyze fields available in each
        recording_fields = set()
        cdr_fields = set()

        for rec in recordings:
            recording_fields.update(rec.keys())

        for cdr in cdr_records:
            cdr_fields.update(cdr.keys())

        # Store analysis
        self.report["analysis"] = {
            "total_recordings": len(recordings),
            "total_cdr_records": len(cdr_records),
            "matched_records": matched,
            "unmatched_recordings": len(unmatched_recordings),
            "recording_fields": sorted(recording_fields),
            "cdr_fields": sorted(cdr_fields),
            "cdr_only_fields": sorted(cdr_fields - recording_fields),
            "recording_only_fields": sorted(recording_fields - cdr_fields),
            "matched_examples": recordings_with_cdr[:3],  # First 3 examples
            "unmatched_examples": unmatched_recordings[:3],
        }

        # Print analysis summary
        print(f"\n   Recording fields: {len(recording_fields)}")
        print(f"   CDR fields: {len(cdr_fields)}")
        print(f"   Matched records: {matched}/{len(recordings)}")

        if cdr_fields - recording_fields:
            print("\n   CDR has additional fields not in recordings:")
            for field in sorted(cdr_fields - recording_fields)[:10]:
                print(f"     - {field}")

        if recording_fields - cdr_fields:
            print("\n   Recordings have fields not in CDR:")
            for field in sorted(recording_fields - cdr_fields)[:10]:
                print(f"     - {field}")

    def _compare_fields(self, recording: Dict, cdr: Dict) -> Dict[str, Any]:
        """Compare fields between recording and CDR"""
        comparison = {}

        # Common fields to compare
        common_fields = ["date", "callerid", "destination", "duration", "rate", "total"]

        for field in common_fields:
            rec_value = recording.get(field)
            cdr_value = cdr.get(field)

            if rec_value is not None or cdr_value is not None:
                comparison[field] = {
                    "recording": rec_value,
                    "cdr": cdr_value,
                    "match": rec_value == cdr_value,
                }

        return comparison

    async def _download_recordings(self, recordings: List[Dict[str, Any]]):
        """Download actual recording files"""
        self.recordings_dir.mkdir(exist_ok=True)

        downloaded = 0
        failed = 0

        for i, rec in enumerate(recordings, 1):
            recording_id = rec.get("recording", rec.get("id"))
            if not recording_id:
                continue

            print(f"   [{i}/{len(recordings)}] Downloading {recording_id}...", end="", flush=True)

            try:
                # Get recording file URL or data
                result = await self.client.getRecordingFile(recording=recording_id)

                if result.get("status") == "success":
                    # The API might return a URL or base64 data
                    if "url" in result:
                        # Download from URL
                        async with httpx.AsyncClient() as http_client:
                            response = await http_client.get(result["url"])
                            response.raise_for_status()

                            # Save file
                            filename = f"{recording_id}.mp3"
                            filepath = self.recordings_dir / filename
                            filepath.write_bytes(response.content)

                            downloaded += 1
                            print(f" ✓ ({len(response.content) / 1024:.1f} KB)")
                    else:
                        print(" ⚠️  No download URL in response")
                        failed += 1
                else:
                    print(f" ✗ {result.get('status', 'error')}")
                    failed += 1

            except Exception as e:
                print(f" ✗ Error: {e}")
                failed += 1

        print(f"\n   Downloaded: {downloaded}, Failed: {failed}")

        self.report["download_stats"] = {
            "attempted": len(recordings),
            "downloaded": downloaded,
            "failed": failed,
            "directory": str(self.recordings_dir),
        }


async def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Inspect VoIP.ms call recordings")
    parser.add_argument(
        "--days", type=int, default=90, help="Days of CDR history to fetch (default: 90)"
    )
    parser.add_argument("--download", action="store_true", help="Download actual recording files")

    args = parser.parse_args()

    if args.download:
        print("⚠️  WARNING: This will download audio files to ./recordings/")
        response = input("Continue? (y/N): ")
        if response.lower() != "y":
            print("Aborted.")
            return

    async with VoIPMSAsyncClient() as client:
        inspector = CallRecordingsInspector(client, args.download)
        report = await inspector.inspect_all(args.days)

        # Print summary
        analysis = report.get("analysis", {})
        if analysis:
            print("\n" + "=" * 50)
            print("Summary:")
            print("=" * 50)
            print(f"Total recordings: {analysis.get('total_recordings', 0)}")
            print(f"Total CDR records: {analysis.get('total_cdr_records', 0)}")
            print(f"Matched records: {analysis.get('matched_records', 0)}")

            if analysis.get("cdr_only_fields"):
                print(f"\n📊 CDR contains {len(analysis['cdr_only_fields'])} additional fields")
                print("   Useful CDR-only fields might include:")
                useful_cdr_fields = ["rate", "total", "seconds", "uniqueid", "disposition"]
                for field in useful_cdr_fields:
                    if field in analysis["cdr_only_fields"]:
                        print(f"   - {field}")


if __name__ == "__main__":
    asyncio.run(main())
