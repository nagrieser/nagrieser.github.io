#!/usr/bin/env python3
"""
ORCID to Zola Publications Exporter

This script fetches publications from an ORCID profile using the ORCID API
and converts them to the format used by the Zola-based academic website.

Author: Mohamed Elashri
Date: 2025-08-31
"""

import requests
import json
import os
import re
import sys
import subprocess
import venv
from pathlib import Path
from datetime import datetime
from urllib.parse import quote
import argparse


def setup_virtual_environment():
    """Set up virtual environment if it doesn't exist and install dependencies"""
    script_dir = Path(__file__).parent
    venv_dir = script_dir / "venv"
    
    if not venv_dir.exists():
        print("Creating virtual environment...")
        venv.create(venv_dir, with_pip=True)
    
    # Get the python executable path in the venv
    if sys.platform == "win32":
        python_exe = venv_dir / "Scripts" / "python.exe"
        pip_exe = venv_dir / "Scripts" / "pip.exe"
    else:
        python_exe = venv_dir / "bin" / "python"
        pip_exe = venv_dir / "bin" / "pip"
    
    # Install requirements if they don't exist
    requirements_file = script_dir / "requirements.txt"
    if requirements_file.exists():
        print("Installing requirements...")
        try:
            subprocess.check_call([str(pip_exe), "install", "-r", str(requirements_file)])
        except subprocess.CalledProcessError as e:
            print(f"Warning: Failed to install requirements: {e}")
    
    return str(python_exe)


def check_and_import_requests():
    """Check if requests is available, if not try to set up venv"""
    try:
        import requests
        return requests
    except ImportError:
        print("requests library not found. Setting up virtual environment...")
        python_exe = setup_virtual_environment()
        
        # Re-run script with venv python
        if python_exe != sys.executable:
            print("Restarting script with virtual environment...")
            subprocess.check_call([python_exe] + sys.argv)
            sys.exit(0)
        else:
            # Try importing again
            try:
                import requests
                return requests
            except ImportError:
                print("Error: Could not install or import requests library")
                print("Please run: pip install requests")
                sys.exit(1)


# Try to import requests, set up venv if needed
requests = check_and_import_requests()


class ORCIDToZola:
    def __init__(self, orcid_id, output_dir="../content/publications"):
        self.orcid_id = orcid_id
        # Convert to absolute path relative to script location
        script_dir = Path(__file__).parent
        self.output_dir = (script_dir / output_dir).resolve()
        self.base_url = "https://pub.orcid.org/v3.0"
        self.headers = {
            'Accept': 'application/json',
            'User-Agent': 'ORCID-to-Zola-Exporter/1.0'
        }
        
    def fetch_orcid_works(self):
        """Fetch works from ORCID profile"""
        works_url = f"{self.base_url}/{self.orcid_id}/works"
        
        try:
            response = requests.get(works_url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching ORCID works: {e}")
            return None
    
    def fetch_work_details(self, put_code):
        """Fetch detailed information for a specific work"""
        work_url = f"{self.base_url}/{self.orcid_id}/work/{put_code}"
        
        try:
            response = requests.get(work_url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching work details for {put_code}: {e}")
            return None
    
    def clean_title(self, title):
        """Clean title for use as folder name - create short, meaningful name"""
        if not title:
            return "untitled"
        
        # First, handle LaTeX commands and mathematical symbols
        latex_replacements = {
            r'\\rightarrow': 'to',
            r'\\leftarrow': 'from',
            r'\\to': 'to',
            r'\\Rightarrow': 'implies',
            r'\\Leftarrow': 'implied-by',
            r'\\leftrightarrow': 'bidirectional',
            r'\\mu': 'mu',
            r'\\nu': 'nu',
            r'\\tau': 'tau',
            r'\\pi': 'pi',
            r'\\sigma': 'sigma',
            r'\\Sigma': 'sigma',
            r'\\lambda': 'lambda',
            r'\\Lambda': 'lambda',
            r'\\gamma': 'gamma',
            r'\\Gamma': 'gamma',
            r'\\alpha': 'alpha',
            r'\\beta': 'beta',
            r'\\delta': 'delta',
            r'\\Delta': 'delta',
            r'\\epsilon': 'epsilon',
            r'\\phi': 'phi',
            r'\\Phi': 'phi',
            r'\\chi': 'chi',
            r'\\psi': 'psi',
            r'\\Psi': 'psi',
            r'\\omega': 'omega',
            r'\\Omega': 'omega',
            r'\\theta': 'theta',
            r'\\Theta': 'theta',
            r'\\xi': 'xi',
            r'\\Xi': 'xi',
            r'\\zeta': 'zeta',
            r'\\eta': 'eta',
            r'\\rho': 'rho',
            r'\\kappa': 'kappa',
            r'\\upsilon': 'upsilon',
            r'\\Upsilon': 'upsilon',
            r'\\_': '',
            r'\\text': '',
            r'\\mathrm': '',
            r'\\mathit': '',
            r'\\mathbf': '',
            r'\\mathcal': '',
            r'\\mathfrak': '',
            r'\\hspace': '',
            r'\\vspace': '',
            r'\\quad': '',
            r'\\qquad': '',
            r'\\,': '',
            r'\\!': '',
            r'\\;': '',
            r'\\:': '',
            r'\\pm': 'plus-minus',
            r'\\mp': 'minus-plus',
            r'\\times': 'times',
            r'\\cdot': 'dot',
            r'\\div': 'div',
            r'\\leq': 'leq',
            r'\\geq': 'geq',
            r'\\neq': 'neq',
            r'\\approx': 'approx',
            r'\\sim': 'sim',
            r'\\propto': 'propto',
            r'\\infty': 'infinity',
            r'\\partial': 'partial',
            r'\\nabla': 'nabla',
            r'\\int': 'integral',
            r'\\sum': 'sum',
            r'\\prod': 'product',
            r'\\sqrt': 'sqrt',
            r'\\frac': '',
            r'\\over': 'over',
            r'\\exp': 'exp',
            r'\\log': 'log',
            r'\\ln': 'ln',
            r'\\sin': 'sin',
            r'\\cos': 'cos',
            r'\\tan': 'tan',
        }
        
        # Apply LaTeX replacements
        cleaned = title
        for latex_cmd, replacement in latex_replacements.items():
            cleaned = re.sub(latex_cmd, replacement, cleaned, flags=re.IGNORECASE)
        
        # Remove remaining LaTeX braces and commands
        cleaned = re.sub(r'\{[^}]*\}', '', cleaned)  # Remove {content}
        cleaned = re.sub(r'\$+', '', cleaned)  # Remove $ symbols
        cleaned = re.sub(r'\\[a-zA-Z]+\*?', '', cleaned)  # Remove remaining \commands (including \var* variants)
        cleaned = re.sub(r'\\[^a-zA-Z]', '', cleaned)  # Remove \symbols
        cleaned = re.sub(r'\^[0-9\+\-]*', '', cleaned)  # Remove superscripts like ^0, ^+, ^-
        cleaned = re.sub(r'_[0-9a-zA-Z\+\-]*', '', cleaned)  # Remove subscripts like _b, _c, _0
        cleaned = re.sub(r'[0-9]+pt', '', cleaned)  # Remove pt measurements like 166656pt
        cleaned = re.sub(r'hspace.*?pt', '', cleaned)  # Remove hspace commands
        
        # Handle special Unicode characters
        unicode_replacements = {
            'Σ': 'sigma',
            'Λ': 'lambda',
            'Ω': 'omega',
            'Γ': 'gamma',
            'Δ': 'delta',
            'Θ': 'theta',
            'Ξ': 'xi',
            'Π': 'pi',
            'Φ': 'phi',
            'Ψ': 'psi',
            'Υ': 'upsilon',
            'σ': 'sigma',
            'λ': 'lambda',
            'ω': 'omega',
            'γ': 'gamma',
            'δ': 'delta',
            'θ': 'theta',
            'ξ': 'xi',
            'π': 'pi',
            'φ': 'phi',
            'ψ': 'psi',
            'υ': 'upsilon',
            'μ': 'mu',
            'ν': 'nu',
            'τ': 'tau',
            'ρ': 'rho',
            'κ': 'kappa',
            'ζ': 'zeta',
            'η': 'eta',
            'χ': 'chi',
            'ε': 'epsilon',
            'α': 'alpha',
            'β': 'beta',
            '→': 'to',
            '←': 'from',
            '↔': 'bidirectional',
            '⇒': 'implies',
            '⇐': 'implied-by',
            '⇔': 'iff',
            '±': 'plus-minus',
            '∓': 'minus-plus',
            '×': 'times',
            '÷': 'div',
            '≤': 'leq',
            '≥': 'geq',
            '≠': 'neq',
            '≈': 'approx',
            '∼': 'sim',
            '∝': 'propto',
            '∞': 'infinity',
            '∂': 'partial',
            '∇': 'nabla',
            '∫': 'integral',
            '∑': 'sum',
            '∏': 'product',
            '√': 'sqrt',
        }
        
        for unicode_char, replacement in unicode_replacements.items():
            cleaned = cleaned.replace(unicode_char, replacement)
        
        # Convert to lowercase and handle remaining special characters
        cleaned = cleaned.lower()
        
        # Remove remaining special characters, keep only letters, numbers, spaces, and hyphens
        cleaned = re.sub(r'[^\w\s-]', '', cleaned)
        
        # Replace spaces with hyphens
        cleaned = re.sub(r'\s+', '-', cleaned)
        
        # Remove multiple consecutive hyphens
        cleaned = re.sub(r'-+', '-', cleaned)
        
        # Remove leading/trailing hyphens
        cleaned = cleaned.strip('-')
        
        # Create a shorter, more meaningful name
        words = cleaned.split('-')
        # Take first few meaningful words, skip common words
        skip_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'between', 'among', 'within', 'without', 'towards', 'upon', 'concerning', 'under', 'over', 'very', 'rare', 'new', 'study', 'analysis', 'measurement', 'observation', 'search'}
        meaningful_words = [word for word in words if word not in skip_words and len(word) > 2]
        
        # Take first 3-4 meaningful words
        short_name = '-'.join(meaningful_words[:4])
        
        return short_name[:50] if short_name else cleaned[:50]  # Limit length
    
    def extract_doi(self, external_ids):
        """Extract DOI from external identifiers"""
        if not external_ids:
            return None
            
        for ext_id in external_ids.get('external-id', []):
            if ext_id.get('external-id-type') == 'doi':
                doi = ext_id.get('external-id-value')
                if doi:
                    # Clean DOI format
                    return doi.replace('https://doi.org/', '').replace('http://dx.doi.org/', '')
        return None
    
    def extract_arxiv_id(self, external_ids):
        """Extract arXiv ID from external identifiers"""
        if not external_ids:
            return None
            
        for ext_id in external_ids.get('external-id', []):
            if ext_id.get('external-id-type') == 'arxiv':
                arxiv_id = ext_id.get('external-id-value')
                if arxiv_id:
                    return arxiv_id
        return None
    
    def extract_inspire_url(self, external_ids):
        """Extract InspireHEP URL from external identifiers"""
        if not external_ids:
            return None
            
        for ext_id in external_ids.get('external-id', []):
            if ext_id.get('external-id-type') == 'other-id':
                url = ext_id.get('external-id-url', {})
                if url and url.get('value') and 'inspirehep.net' in url.get('value'):
                    return url.get('value')
        return None
    
    def extract_work_url(self, work_detail):
        """Extract work URL from work detail"""
        url = work_detail.get('url', {})
        if url and url.get('value'):
            return url.get('value')
        return None
    
    def is_lhcb_collaboration_paper(self, work_detail):
        """Check if this is an LHCb collaboration paper"""
        # Check title
        title = work_detail.get('title', {}).get('title', {}).get('value', '').lower()
        if 'lhcb' in title:
            return True
            
        # Check journal
        journal = work_detail.get('journal-title', {})
        if journal and 'lhcb' in journal.get('value', '').lower():
            return True
            
        # Check if we have a very large number of authors (typical for LHCb)
        contributors = work_detail.get('contributors', {}).get('contributor', [])
        if len(contributors) > 100:  # LHCb papers typically have 800+ authors
            return True
            
        return False
    
    def extract_authors(self, contributors, work_detail=None):
        """Extract authors from contributors, handle LHCb collaboration specially"""
        authors = []
        if not contributors:
            return authors
            
        all_authors = []
        for contributor in contributors.get('contributor', []):
            credit_name = contributor.get('credit-name')
            if credit_name and credit_name.get('value'):
                name = credit_name['value']
                all_authors.append(name)
        
        # Check if this is an LHCb collaboration paper
        if work_detail and self.is_lhcb_collaboration_paper(work_detail):
            return ["M. Elashri", "LHCb Collaboration"]
            
        # Check if this is a large collaboration (general case)
        if len(all_authors) > 20:  # Threshold for collaboration papers
            # For other large collaborations, show first few authors + et al
            return all_authors[:3] + ["et al."]
        
        # For regular papers with reasonable author count
        return all_authors[:10]  # Limit to 10 authors max
    
    def extract_publication_year(self, publication_date):
        """Extract publication year"""
        if not publication_date:
            return None
            
        year = publication_date.get('year')
        if year and year.get('value'):
            return year['value']
        return None
    
    def format_date(self, publication_date):
        """Format publication date for Zola frontmatter"""
        if not publication_date:
            return datetime.now().strftime("%Y-%m-%d")
            
        year = publication_date.get('year', {}).get('value')
        month = publication_date.get('month', {}).get('value', 1)
        day = publication_date.get('day', {}).get('value', 1)
        
        try:
            date_obj = datetime(int(year or datetime.now().year), 
                              int(month or 1), 
                              int(day or 1))
            return date_obj.strftime("%Y-%m-%d")
        except (ValueError, TypeError):
            return datetime.now().strftime("%Y-%m-%d")
    
    def clean_latex_for_display(self, text):
        """Clean LaTeX for better display by removing excessive spacing and commands"""
        if not text:
            return text
        
        # Remove excessive spacing commands that make titles ugly
        text = re.sub(r'\\hspace\{[^}]+\}', '', text)  # Remove \hspace{...}
        text = re.sub(r'\\!', '', text)  # Remove negative thin space
        text = re.sub(r'\\,', ' ', text)  # Replace thin space with regular space
        text = re.sub(r'\\;', ' ', text)  # Replace medium space with regular space
        text = re.sub(r'\\:', ' ', text)  # Replace medium space with regular space
        text = re.sub(r'\\quad', ' ', text)  # Replace quad space with regular space
        text = re.sub(r'\\qquad', '  ', text)  # Replace double quad with double space
        
        # Clean up multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Remove some complex bracing that doesn't display well
        text = re.sub(r'\{\{\{([^}]+)\}\}\}', r'\1', text)  # {{{content}}} -> content
        text = re.sub(r'\{\{([^}]+)\}\}', r'\1', text)  # {{content}} -> content
        
        return text.strip()
    
    def convert_latex_to_mathml(self, text):
        """Convert LaTeX math expressions to MathML"""
        if not text:
            return text
            
        # Simple LaTeX to MathML conversion for common cases
        # This is a basic implementation - you might want to use a proper library like latexml
        
        # Inline math: $...$
        def replace_inline_math(match):
            content = match.group(1)
            return f'<math xmlns="http://www.w3.org/1998/Math/MathML"><mrow>{content}</mrow></math>'
        
        # Display math: $$...$$
        def replace_display_math(match):
            content = match.group(1)
            return f'<math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mrow>{content}</mrow></math>'
        
        # Replace display math first
        text = re.sub(r'\$\$(.*?)\$\$', replace_display_math, text, flags=re.DOTALL)
        # Then inline math
        text = re.sub(r'\$(.*?)\$', replace_inline_math, text)
        
        return text
    
    def generate_bibtex(self, work_detail):
        """Generate BibTeX entry from work details"""
        title = work_detail.get('title', {}).get('title', {}).get('value', 'Untitled')
        authors = self.extract_authors(work_detail.get('contributors'), work_detail)
        year = self.extract_publication_year(work_detail.get('publication-date'))
        doi = self.extract_doi(work_detail.get('external-ids'))
        
        # Create a simple BibTeX key
        first_author = authors[0].split()[-1] if authors else "author"
        bibtex_key = f"{first_author.lower()}_{year or 'unknown'}_{self.clean_title(title)[:20]}"
        
        bibtex = f"""@article{{{bibtex_key},
    title = {{{title}}},
    author = {{{' and '.join(authors)}}},
    year = {{{year or 'unknown'}}},"""
        
        if doi:
            bibtex += f"\n    doi = {{{doi}}},"
            bibtex += f"\n    url = {{https://doi.org/{doi}}},"
        
        bibtex += "\n}"
        
        return bibtex
    
    def create_publication_folder(self, work_detail):
        """Create publication folder and files with format: {year}-{short-name}"""
        title = work_detail.get('title', {}).get('title', {}).get('value', 'Untitled')
        year = self.extract_publication_year(work_detail.get('publication-date'))
        
        # Create folder name with year-short-name format
        short_name = self.clean_title(title)
        folder_name = f"{year or 'unknown'}-{short_name}"
        folder_path = self.output_dir / folder_name
        
        # Check if folder already exists
        if folder_path.exists():
            return None  # Signal that folder was skipped
        
        # Create folder
        folder_path.mkdir(parents=True, exist_ok=True)
        
        # Extract publication details
        authors = self.extract_authors(work_detail.get('contributors'), work_detail)
        publication_date = self.format_date(work_detail.get('publication-date'))
        external_ids = work_detail.get('external-ids', {})
        doi = self.extract_doi(external_ids)
        arxiv_id = self.extract_arxiv_id(external_ids)
        inspire_url = self.extract_inspire_url(external_ids)
        work_url = self.extract_work_url(work_detail)
        abstract = work_detail.get('short-description', '')
        
        # Get journal/conference info
        journal_title = work_detail.get('journal-title', {})
        if journal_title and journal_title.get('value'):
            publication_venue = journal_title['value']
        else:
            publication_venue = "Unknown Venue"
        
        # Determine publication type
        work_type = work_detail.get('type', 'journal-article')
        if 'conference' in work_type.lower():
            pub_type = "Conference Paper"
        elif 'book' in work_type.lower():
            pub_type = "Book Chapter"
        else:
            pub_type = "Journal Article"
        
        # Convert abstract LaTeX to MathML
        if abstract:
            abstract = self.convert_latex_to_mathml(abstract)
        
        # Create a cleaned display title by removing excessive LaTeX spacing commands
        display_title = self.clean_latex_for_display(title) if ('\\' in title or '$' in title) else title
        
        # Handle title escaping for TOML - use literal strings for complex titles with LaTeX
        if '\\' in title or '$' in title:
            # Use TOML literal string (single quotes) for titles with backslashes
            escaped_title = title.replace("'", "\\'")
            title_line = f"title = '{escaped_title}'"
        elif len(title) > 100:
            # Use triple-quoted string for long titles without backslashes
            escaped_title = title.replace('"""', '\\"""')
            title_line = f'title = """{escaped_title}"""'
        else:
            # Use regular quoted string for simple titles
            escaped_title = title.replace('"', '\\"')
            title_line = f'title = "{escaped_title}"'
        
        # Add display title for LaTeX rendering if different
        if display_title != title:
            # Use literal string (single quotes) for LaTeX content to avoid escaping issues
            escaped_display_title = display_title.replace("'", "\\'")
            display_title_line = f"\ndisplay_title = '{escaped_display_title}'"
        else:
            display_title_line = ""
        
        # Escape publication venue for TOML
        escaped_publication_venue = publication_venue.replace('\\', '\\\\').replace('"', '\\"')
        
        # Create index.md
        frontmatter = f'''+++
{title_line}{display_title_line}
date = "{publication_date}"
[taxonomies]
tags = ["Research"]
authors = {json.dumps(authors)}
[extra]
publication = "{escaped_publication_venue}"
publication_type = "{pub_type}"'''
        
        if abstract:
            frontmatter += f'\nabstract = """{abstract}"""'
        
        # Add links
        links = []
        
        # Add DOI link if available
        if doi:
            links.append({
                "url": f"https://doi.org/{doi}",
                "name": "DOI",
                "icon": "web"
            })
            # Note: Zotero button is automatically added by the template for DOI links
        
        # Add arXiv link if available
        if arxiv_id:
            links.append({
                "url": f"https://arxiv.org/abs/{arxiv_id}",
                "name": "arXiv",
                "icon": "text"
            })
        
        # Add InspireHEP link if available
        if inspire_url:
            links.append({
                "url": inspire_url,
                "name": "InspireHEP",
                "icon": "web"
            })
        
        # Add work URL if available and different from InspireHEP
        if work_url and work_url != inspire_url:
            links.append({
                "url": work_url,
                "name": "Publisher's Website",
                "icon": "web"
            })
        
        # Always include links field (even if empty) to avoid template errors
        if links:
            # Format links as TOML inline tables
            links_str = "[\n"
            for link in links:
                links_str += f'    {{url = "{link["url"]}", name = "{link["name"]}", icon = "{link["icon"]}"}},\n'
            links_str += "]"
            frontmatter += f'\nlinks = {links_str}'
        else:
            frontmatter += '\nlinks = []'
        
        frontmatter += '\n+++'
        
        # Write index.md
        index_path = folder_path / "index.md"
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter)
        
        # Create cite.bib
        bibtex = self.generate_bibtex(work_detail)
        cite_path = folder_path / "cite.bib"
        with open(cite_path, 'w', encoding='utf-8') as f:
            f.write(bibtex)
        
        return folder_path
    
    def export_publications(self, test_count=None):
        """Main method to export publications"""
        print(f"🔍 Fetching publications for ORCID ID: {self.orcid_id}")
        
        # Fetch works list
        works_data = self.fetch_orcid_works()
        if not works_data:
            print("❌ Failed to fetch works from ORCID")
            return
        
        works_group = works_data.get('group', [])
        if not works_group:
            print("⚠️  No publications found")
            return
        
        total_pubs = len(works_group)
        print(f"📚 Found {total_pubs} publication groups")
        
        # Limit for testing if specified
        if test_count is not None:
            works_group = works_group[:test_count]
            print(f"🧪 Testing mode: Processing only {len(works_group)} publications")
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        print(f"📁 Output directory: {self.output_dir}")
        
        created_count = 0
        skipped_count = 0
        error_count = 0
        
        for i, group in enumerate(works_group, 1):
            print(f"\n📄 Processing publication {i}/{total_pubs}...")
            
            work_summary = group.get('work-summary', [])
            if work_summary:
                # Get the first work summary (usually the most recent)
                put_code = work_summary[0].get('put-code')
                if put_code:
                    # Fetch detailed information
                    work_detail = self.fetch_work_details(put_code)
                    if work_detail:
                        try:
                            title = work_detail.get('title', {}).get('title', {}).get('value', 'Untitled')
                            print(f"   Title: {title[:60]}{'...' if len(title) > 60 else ''}")
                            
                            folder_path = self.create_publication_folder(work_detail)
                            if folder_path:
                                created_count += 1
                                print(f"   ✅ Created: {folder_path.name}")
                            else:
                                skipped_count += 1
                                print(f"   ⏭️  Skipped: Already exists")
                        except Exception as e:
                            error_count += 1
                            print(f"   ❌ Error: {e}")
                    else:
                        error_count += 1
                        print(f"   ❌ Failed to fetch details for put-code: {put_code}")
                else:
                    error_count += 1
                    print(f"   ❌ No put-code found")
            else:
                error_count += 1
                print(f"   ❌ No work summary found")
        
        print(f"\n🎉 Export completed!")
        print(f"   ✅ Created: {created_count} publications")
        print(f"   ⏭️  Skipped: {skipped_count} publications (already exist)")
        print(f"   ❌ Errors: {error_count} publications")
        print(f"   📁 Location: {self.output_dir}")
        
        if created_count > 0:
            print(f"\n💡 Next steps:")
            print(f"   1. Review the generated publications in {self.output_dir}")
            print(f"   2. Run 'zola serve' to preview your site")
            print(f"   3. Commit and push the changes to deploy")


def main():
    parser = argparse.ArgumentParser(description='Export ORCID publications to Zola format')
    parser.add_argument('--orcid-id', default='0000-0001-9398-953X',
                        help='ORCID ID (default: 0000-0001-9398-953X)')
    parser.add_argument('--output-dir', default='../content/publications',
                        help='Output directory relative to scripts folder (default: ../content/publications)')
    parser.add_argument('--test-count', type=int, default=None,
                        help='Limit number of publications to process for testing')
    
    args = parser.parse_args()
    
    # Validate ORCID ID format
    orcid_pattern = r'^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$'
    if not re.match(orcid_pattern, args.orcid_id):
        print(f"Invalid ORCID ID format: {args.orcid_id}")
        print("Expected format: 0000-0000-0000-0000")
        sys.exit(1)
    
    exporter = ORCIDToZola(args.orcid_id, args.output_dir)
    exporter.export_publications(test_count=args.test_count)


if __name__ == "__main__":
    main()
