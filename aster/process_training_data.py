#!/usr/bin/env python3
"""
Batch Process Training Data for Aster
Processes all files in tests/training_data folder recursively
"""

import subprocess
import time
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List

class TrainingDataProcessor:
    def __init__(self, training_folder: Path = None, output_folder: Path = None):
        self.script_dir = Path(__file__).parent
        self.training_folder = training_folder or self.script_dir / "tests" / "training_data"
        self.output_folder = output_folder or self.script_dir / "tests" / "training_outputs"
        self.aster_script = self.script_dir / "aster.py"
        self.results = []

        # Create output folder if it doesn't exist
        self.output_folder.mkdir(parents=True, exist_ok=True)

        # File categorization
        self.categories = {
            'spreadsheet': ['.xlsx', '.xls'],
            'audio': ['.wma', '.mp3', '.wav', '.m4a', '.flac', '.ogg'],
            'image': ['.jpg', '.jpeg', '.png', '.gif', '.tiff', '.tif', '.bmp'],
            'document': ['.docx', '.doc', '.odt', '.rtf'],
            'pdf': ['.pdf'],
            'presentation': ['.pptx', '.ppt'],
            'ebook': ['.epub', '.mobi'],
            'web': ['.html', '.htm', '.mhtml'],
            'text': ['.txt', '.md', '.markdown'],
            'csv': ['.csv']
        }

    def get_category(self, file_path: Path) -> str:
        """Determine file category"""
        suffix = file_path.suffix.lower()
        for category, extensions in self.categories.items():
            if suffix in extensions:
                return category
        return 'unknown'

    def get_all_files(self) -> List[Path]:
        """Get all processable files from training_data folder recursively"""
        files = []

        if not self.training_folder.exists():
            print(f"❌ Training folder not found: {self.training_folder}")
            return files

        # Get all files recursively
        for item in self.training_folder.rglob('*'):
            if item.is_file():
                # Skip hidden files, README, and non-processable files
                if (not item.name.startswith('.') and
                    item.suffix.lower() not in ['.py', '.json', '.gitkeep'] and
                    item.name.lower() not in ['readme.md', 'readme.txt']):
                    files.append(item)

        return sorted(files)

    def process_single_file(self, input_file: Path) -> Dict:
        """Process a single file with Aster"""
        # Calculate relative path for better organization
        rel_path = input_file.relative_to(self.training_folder)

        print(f"\n{'='*80}")
        print(f"Processing: {rel_path}")
        print(f"Size: {input_file.stat().st_size / 1024:.1f} KB")
        print(f"Category: {self.get_category(input_file)}")
        print(f"{'='*80}")

        # Create output path maintaining folder structure
        output_path = self.output_folder / rel_path.parent / f"{input_file.stem}.md"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        result = {
            'filename': str(rel_path),
            'absolute_path': str(input_file),
            'size_kb': round(input_file.stat().st_size / 1024, 1),
            'category': self.get_category(input_file),
            'timestamp': datetime.now().isoformat()
        }

        # Run Aster processor
        start_time = time.time()
        try:
            cmd = [
                sys.executable,
                str(self.aster_script),
                str(input_file),
                '-o', str(output_path),
                '--model', 'llama3.2:1b'
            ]

            print(f"Command: {' '.join(cmd)}\n")

            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout for large files
            )

            elapsed = time.time() - start_time
            result['processing_time'] = round(elapsed, 2)
            result['exit_code'] = process.returncode
            result['stdout'] = process.stdout
            result['stderr'] = process.stderr

            # Check if output was created
            if output_path.exists():
                result['success'] = True
                result['output_size_kb'] = round(output_path.stat().st_size / 1024, 1)
                result['output_file'] = str(output_path.relative_to(self.output_folder))

                # Quality check
                with open(output_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    result['output_lines'] = len(content.split('\n'))
                    result['output_chars'] = len(content)
                    result['has_frontmatter'] = content.startswith('---')
                    result['has_headings'] = '#' in content

                print(f"✅ SUCCESS in {elapsed:.1f}s")
                print(f"   Output: {result['output_file']} ({result['output_size_kb']} KB)")
                print(f"   Lines: {result['output_lines']}, Chars: {result['output_chars']}")
            else:
                result['success'] = False
                result['error'] = 'Output file not created'
                print(f"❌ FAILED: Output not created")

        except subprocess.TimeoutExpired:
            elapsed = time.time() - start_time
            result['processing_time'] = round(elapsed, 2)
            result['success'] = False
            result['error'] = f'Timeout after {elapsed:.0f} seconds'
            print(f"⏱️  TIMEOUT after {elapsed:.1f}s")

        except Exception as e:
            elapsed = time.time() - start_time
            result['processing_time'] = round(elapsed, 2)
            result['success'] = False
            result['error'] = str(e)
            print(f"💥 ERROR: {e}")

        # Print diagnostics for failures
        if not result.get('success', False):
            if result.get('stderr'):
                print(f"\nSTDERR:\n{result['stderr']}")
            if result.get('stdout'):
                print(f"\nSTDOUT:\n{result['stdout']}")

        return result

    def generate_report(self):
        """Generate comprehensive processing report"""
        report_path = self.script_dir / "tests" / "TRAINING_DATA_RESULTS.md"
        json_path = self.script_dir / "tests" / "training_data_results.json"

        # Save JSON results
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2)

        # Calculate statistics
        total = len(self.results)
        if total == 0:
            print("No files processed!")
            return

        successful = sum(1 for r in self.results if r.get('success', False))
        failed = total - successful
        total_time = sum(r.get('processing_time', 0) for r in self.results)

        # Stats by category
        categories = {}
        for result in self.results:
            cat = result['category']
            if cat not in categories:
                categories[cat] = {'total': 0, 'success': 0, 'failed': 0, 'total_time': 0}
            categories[cat]['total'] += 1
            if result.get('success', False):
                categories[cat]['success'] += 1
            else:
                categories[cat]['failed'] += 1
            categories[cat]['total_time'] += result.get('processing_time', 0)

        # Generate markdown report
        report = f"""# Training Data Processing Report

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Folder: {self.training_folder}

## Summary

- **Total Files Processed**: {total}
- **Successful**: {successful} ({successful/total*100:.1f}%)
- **Failed**: {failed} ({failed/total*100:.1f}%)
- **Total Processing Time**: {total_time/60:.1f} minutes
- **Average Time per File**: {total_time/total:.1f} seconds
- **Success Rate**: {'✅ EXCELLENT' if successful/total > 0.8 else '⚠️ NEEDS WORK' if successful/total > 0.5 else '❌ POOR'}

## Results by Category

"""
        for cat, stats in sorted(categories.items()):
            success_rate = stats['success'] / stats['total'] * 100 if stats['total'] > 0 else 0
            avg_time = stats['total_time'] / stats['total'] if stats['total'] > 0 else 0
            report += f"""### {cat.title()}
- Files: {stats['total']}
- Success: {stats['success']}/{stats['total']} ({success_rate:.0f}%)
- Total Time: {stats['total_time']/60:.1f} min
- Avg Time: {avg_time:.1f}s per file
- Status: {'✅' if success_rate == 100 else '⚠️' if success_rate > 50 else '❌'}

"""

        report += "## Failed Files\n\n"
        failed_files = [r for r in self.results if not r.get('success', False)]
        if failed_files:
            for result in sorted(failed_files, key=lambda x: x['filename']):
                report += f"### ❌ {result['filename']}\n"
                report += f"- **Category**: {result['category']}\n"
                report += f"- **Size**: {result['size_kb']} KB\n"
                report += f"- **Error**: {result.get('error', 'Unknown error')}\n\n"
        else:
            report += "No failures! 🎉\n\n"

        report += f"""
## Common Issues Found

"""
        # Identify common errors
        error_types = {}
        for result in failed_files:
            error = result.get('error', 'Unknown')
            if 'ffmpeg' in error.lower():
                error_types['ffmpeg'] = error_types.get('ffmpeg', 0) + 1
            elif 'pandoc' in error.lower():
                error_types['pandoc'] = error_types.get('pandoc', 0) + 1
            elif 'timeout' in error.lower():
                error_types['timeout'] = error_types.get('timeout', 0) + 1
            elif 'not installed' in error.lower():
                error_types['missing_dependency'] = error_types.get('missing_dependency', 0) + 1
            else:
                error_types['other'] = error_types.get('other', 0) + 1

        if error_types:
            if 'ffmpeg' in error_types:
                report += f"- **ffmpeg missing**: {error_types['ffmpeg']} files (install with `brew install ffmpeg`)\n"
            if 'pandoc' in error_types:
                report += f"- **pandoc missing**: {error_types['pandoc']} files (install with `brew install pandoc`)\n"
            if 'timeout' in error_types:
                report += f"- **timeouts**: {error_types['timeout']} files (consider increasing timeout)\n"
            if 'missing_dependency' in error_types:
                report += f"- **missing dependencies**: {error_types['missing_dependency']} files\n"
            if 'other' in error_types:
                report += f"- **other errors**: {error_types['other']} files\n"
        else:
            report += "No common issues found!\n"

        report += f"""
## Next Steps

1. Install missing system dependencies (ffmpeg, pandoc, etc.)
2. Review failed files and categorize issues
3. Optimize Ollama prompts based on successful outputs
4. Create quality metrics for output validation
5. Consider parallel processing for large batches

## Raw Data

Full results saved to: `training_data_results.json`
Output files saved to: `{self.output_folder.relative_to(self.script_dir)}`
"""

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"\n{'='*80}")
        print(f"📊 Report generated: {report_path}")
        print(f"📊 JSON data saved: {json_path}")
        print(f"📂 Output folder: {self.output_folder}")
        print(f"{'='*80}")

    def process_all(self):
        """Process all training data files"""
        files = self.get_all_files()

        if not files:
            print(f"❌ No files found in {self.training_folder}")
            return

        print(f"\n🚀 Found {len(files)} files to process\n")
        print(f"📂 Training folder: {self.training_folder}")
        print(f"📂 Output folder: {self.output_folder}\n")

        # Process each file
        for i, file_path in enumerate(files, 1):
            print(f"\n[{i}/{len(files)}]")
            result = self.process_single_file(file_path)
            self.results.append(result)

        # Generate report
        self.generate_report()

        # Print summary
        successful = sum(1 for r in self.results if r.get('success', False))
        total = len(self.results)
        total_time = sum(r.get('processing_time', 0) for r in self.results)

        print(f"\n{'='*80}")
        print(f"🎯 Processing Summary:")
        print(f"   Total: {total} files")
        print(f"   Success: {successful} ({successful/total*100:.1f}%)")
        print(f"   Failed: {total - successful}")
        print(f"   Time: {total_time/60:.1f} minutes")
        print(f"{'='*80}\n")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Process training data folder')
    parser.add_argument('--folder', type=Path, help='Training data folder path (default: tests/training_data)')
    parser.add_argument('--output', type=Path, help='Output folder path (default: tests/training_outputs)')
    parser.add_argument('--resume', action='store_true', help='Resume from previous run (skip already processed)')

    args = parser.parse_args()

    processor = TrainingDataProcessor(
        training_folder=args.folder,
        output_folder=args.output
    )

    processor.process_all()
