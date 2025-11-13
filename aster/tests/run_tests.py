#!/usr/bin/env python3
"""
Test Runner for Aster
Processes all test files and generates comprehensive report
"""

import subprocess
import time
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

class TestRunner:
    def __init__(self):
        self.test_dir = Path(__file__).parent
        self.output_dir = self.test_dir / "outputs"
        self.script_path = self.test_dir.parent / "aster.py"
        self.results = []

        # File categorization
        self.categories = {
            'spreadsheet': ['.xlsx', '.xls'],
            'audio': ['.wma', '.mp3', '.wav', '.m4a'],
            'image': ['.jpg', '.jpeg', '.png', '.gif'],
            'document': ['.docx', '.doc', '.odt'],
            'pdf': ['.pdf'],
            'presentation': ['.pptx', '.ppt'],
            'ebook': ['.epub', '.mobi'],
            'web': ['.html', '.htm'],
            'text': ['.txt', '.md'],
            'csv': ['.csv']
        }

    def get_category(self, file_path: Path) -> str:
        """Determine file category"""
        suffix = file_path.suffix.lower()
        for category, extensions in self.categories.items():
            if suffix in extensions:
                return category
        return 'unknown'

    def get_test_files(self) -> List[Path]:
        """Get all test files (excluding outputs and scripts)"""
        test_files = []
        for file_path in self.test_dir.iterdir():
            if file_path.is_file() and file_path.suffix not in ['.py', '.md', '.json']:
                test_files.append(file_path)
        return sorted(test_files)

    def run_single_test(self, input_file: Path) -> Dict:
        """Run mdclean_universal on a single file"""
        print(f"\n{'='*80}")
        print(f"Testing: {input_file.name}")
        print(f"Size: {input_file.stat().st_size / 1024:.1f} KB")
        print(f"Category: {self.get_category(input_file)}")
        print(f"{'='*80}")

        output_file = self.output_dir / f"{input_file.stem}.md"

        result = {
            'filename': input_file.name,
            'size_kb': round(input_file.stat().st_size / 1024, 1),
            'category': self.get_category(input_file),
            'timestamp': datetime.now().isoformat()
        }

        # Run the processor
        start_time = time.time()
        try:
            cmd = [
                sys.executable,  # Use same Python interpreter (respects venv)
                str(self.script_path),
                str(input_file),
                '-o', str(output_file),
                '--model', 'llama3.2:1b'
            ]

            print(f"Command: {' '.join(cmd)}\n")

            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            elapsed = time.time() - start_time
            result['processing_time'] = round(elapsed, 2)
            result['exit_code'] = process.returncode
            result['stdout'] = process.stdout
            result['stderr'] = process.stderr

            # Check if output was created
            if output_file.exists():
                result['success'] = True
                result['output_size_kb'] = round(output_file.stat().st_size / 1024, 1)
                result['output_file'] = str(output_file.name)

                # Quick quality check
                with open(output_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    result['output_lines'] = len(content.split('\n'))
                    result['output_chars'] = len(content)
                    result['has_frontmatter'] = content.startswith('---')
                    result['has_headings'] = '#' in content

                print(f"✅ SUCCESS in {elapsed:.1f}s")
                print(f"   Output: {output_file.name} ({result['output_size_kb']} KB)")
                print(f"   Lines: {result['output_lines']}, Chars: {result['output_chars']}")
            else:
                result['success'] = False
                result['error'] = 'Output file not created'
                print(f"❌ FAILED: Output not created")

        except subprocess.TimeoutExpired:
            elapsed = time.time() - start_time
            result['processing_time'] = round(elapsed, 2)
            result['success'] = False
            result['error'] = 'Timeout after 5 minutes'
            print(f"⏱️  TIMEOUT after {elapsed:.1f}s")

        except Exception as e:
            elapsed = time.time() - start_time
            result['processing_time'] = round(elapsed, 2)
            result['success'] = False
            result['error'] = str(e)
            print(f"💥 ERROR: {e}")

        # Print stdout/stderr if there were issues
        if not result.get('success', False):
            if result.get('stderr'):
                print(f"\nSTDERR:\n{result['stderr']}")
            if result.get('stdout'):
                print(f"\nSTDOUT:\n{result['stdout']}")

        return result

    def generate_report(self):
        """Generate comprehensive test report"""
        report_path = self.test_dir / "TEST_RESULTS.md"
        json_path = self.test_dir / "test_results.json"

        # Save JSON results
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2)

        # Generate markdown report
        total = len(self.results)
        successful = sum(1 for r in self.results if r.get('success', False))
        failed = total - successful

        # Calculate stats by category
        categories = {}
        for result in self.results:
            cat = result['category']
            if cat not in categories:
                categories[cat] = {'total': 0, 'success': 0, 'failed': 0, 'avg_time': 0}
            categories[cat]['total'] += 1
            if result.get('success', False):
                categories[cat]['success'] += 1
            else:
                categories[cat]['failed'] += 1
            categories[cat]['avg_time'] += result.get('processing_time', 0)

        for cat in categories:
            if categories[cat]['total'] > 0:
                categories[cat]['avg_time'] /= categories[cat]['total']
                categories[cat]['avg_time'] = round(categories[cat]['avg_time'], 2)

        report = f"""# Test Results Report

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary

- **Total Files Tested**: {total}
- **Successful**: {successful} ({successful/total*100:.1f}%)
- **Failed**: {failed} ({failed/total*100:.1f}%)
- **Success Rate**: {'✅ EXCELLENT' if successful/total > 0.8 else '⚠️ NEEDS WORK' if successful/total > 0.5 else '❌ POOR'}

## Results by Category

"""
        for cat, stats in sorted(categories.items()):
            success_rate = stats['success'] / stats['total'] * 100 if stats['total'] > 0 else 0
            report += f"""### {cat.title()}
- Files: {stats['total']}
- Success: {stats['success']}/{stats['total']} ({success_rate:.0f}%)
- Avg Time: {stats['avg_time']:.2f}s
- Status: {'✅' if success_rate == 100 else '⚠️' if success_rate > 50 else '❌'}

"""

        report += "## Individual Test Results\n\n"

        for result in sorted(self.results, key=lambda x: (x['category'], x['filename'])):
            status = '✅' if result.get('success', False) else '❌'
            report += f"""### {status} {result['filename']}

- **Category**: {result['category']}
- **Size**: {result['size_kb']} KB
- **Time**: {result.get('processing_time', 'N/A')}s
- **Status**: {"SUCCESS" if result.get('success', False) else "FAILED"}
"""
            if result.get('success', False):
                report += f"""- **Output**: {result['output_file']} ({result['output_size_kb']} KB)
- **Lines**: {result['output_lines']}
- **Has Frontmatter**: {result['has_frontmatter']}
- **Has Headings**: {result['has_headings']}
"""
            else:
                report += f"- **Error**: {result.get('error', 'Unknown error')}\n"

            report += "\n"

        # Add recommendations
        report += """## Recommendations

### Format Support Issues
"""
        for result in self.results:
            if not result.get('success', False) and 'not supported' in result.get('error', '').lower():
                report += f"- Add support for {result['category']} (.{result['filename'].split('.')[-1]})\n"

        report += """
### Ollama Prompt Optimization Needed
Based on test results, create specialized prompts for:

1. **Religious/Theological Content** (Afrikaans)
   - Preserve proper nouns (church names, people, places)
   - Maintain theological terminology
   - Respect formatting of prayers and liturgical texts

2. **Books and Long Documents**
   - Better chapter detection
   - Preserve heading hierarchy
   - Maintain references and footnotes

3. **Technical Documents**
   - Preserve code blocks
   - Maintain list formatting
   - Keep technical terminology

4. **Multilingual Content**
   - Detect language and adjust accordingly
   - Preserve language-specific characters
   - Don't over-correct proper nouns

### Performance Improvements
"""
        large_files = [r for r in self.results if r['size_kb'] > 500]
        if large_files:
            report += "- Add progress indicators for large files:\n"
            for r in large_files:
                report += f"  - {r['filename']} ({r['size_kb']} KB took {r.get('processing_time', 'N/A')}s)\n"

        report += f"""
### Next Steps

1. Fix format support issues
2. Create specialized Ollama prompts
3. Add automated quality validation
4. Implement progress indicators for large files
5. Create pytest suite for regression testing

## Raw Data

Full test results saved to: `test_results.json`
"""

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"\n{'='*80}")
        print(f"📊 Report generated: {report_path}")
        print(f"📊 JSON data saved: {json_path}")
        print(f"{'='*80}")

    def run_all_tests(self):
        """Run all tests and generate report"""
        test_files = self.get_test_files()
        print(f"\n🧪 Found {len(test_files)} test files\n")

        for test_file in test_files:
            result = self.run_single_test(test_file)
            self.results.append(result)

        self.generate_report()

        # Print summary
        successful = sum(1 for r in self.results if r.get('success', False))
        total = len(self.results)
        print(f"\n{'='*80}")
        print(f"🎯 Test Summary: {successful}/{total} successful ({successful/total*100:.1f}%)")
        print(f"{'='*80}\n")


if __name__ == '__main__':
    runner = TestRunner()
    runner.run_all_tests()
