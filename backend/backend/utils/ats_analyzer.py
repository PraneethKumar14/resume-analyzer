import re

class ATSAnalyzer:
    def __init__(self):
        # Comprehensive keyword lists
        self.technical_skills = [
            # Programming Languages
            'python', 'javascript', 'java', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin', 'go', 'rust', 'typescript',
            # Web Technologies
            'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'spring', 'laravel',
            # Databases
            'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sqlite', 'cassandra',
            # Cloud & DevOps
            'aws', 'azure', 'google cloud', 'docker', 'kubernetes', 'jenkins', 'gitlab', 'github actions', 'terraform',
            'ansible', 'nginx', 'apache', 'linux', 'bash', 'powershell',
            # Data & ML
            'machine learning', 'deep learning', 'neural networks', 'tensorflow', 'pytorch', 'scikit-learn', 'pandas',
            'numpy', 'matplotlib', 'seaborn', 'data analysis', 'data visualization', 'big data', 'hadoop', 'spark',
            # Other Important Skills
            'api', 'rest', 'graphql', 'microservices', 'agile', 'scrum', 'git', 'github', 'bitbucket', 'jira',
            'testing', 'unit testing', 'integration testing', 'cybersecurity', 'network security', 'blockchain'
        ]
        
        self.action_verbs = [
            'achieved', 'accelerated', 'accomplished', 'adapted', 'administered', 'analyzed', 'applied', 'approved',
            'arranged', 'assembled', 'assessed', 'assigned', 'assisted', 'attained', 'audited', 'balanced', 'boosted',
            'built', 'calculated', 'cataloged', 'charted', 'classified', 'collaborated', 'collected', 'communicated',
            'compared', 'compiled', 'completed', 'computed', 'conceived', 'concluded', 'conducted', 'constructed',
            'consulted', 'contracted', 'controlled', 'converted', 'conveyed', 'created', 'critiqued', 'debugged',
            'decreased', 'defined', 'delivered', 'demonstrated', 'deployed', 'designed', 'developed', 'devised',
            'diagnosed', 'directed', 'discovered', 'dispatched', 'displayed', 'diversified', 'documented', 'earned',
            'edited', 'educated', 'eliminated', 'employed', 'enabled', 'encouraged', 'engineered', 'enhanced',
            'enlisted', 'ensured', 'established', 'estimated', 'evaluated', 'examined', 'executed', 'expanded',
            'experimented', 'explained', 'explored', 'extracted', 'fabricated', 'facilitated', 'fashioned', 'fielded',
            'filed', 'filled', 'financed', 'forecast', 'formulated', 'founded', 'fulfilled', 'generated', 'grew',
            'guided', 'handled', 'headed', 'helped', 'identified', 'illustrated', 'implemented', 'improved',
            'increased', 'initiated', 'innovated', 'inspected', 'inspired', 'installed', 'instructed', 'integrated',
            'interpreted', 'interviewed', 'introduced', 'invented', 'investigated', 'joined', 'launched', 'led',
            'lectured', 'located', 'maintained', 'managed', 'marketed', 'maximized', 'measured', 'mediated',
            'modified', 'motivated', 'negotiated', 'observed', 'obtained', 'operated', 'optimized', 'organized',
            'originated', 'overhauled', 'oversaw', 'participated', 'perceived', 'performed', 'persuaded', 'pioneered',
            'planned', 'predicted', 'prepared', 'presented', 'processed', 'produced', 'programmed', 'projected',
            'promoted', 'proofread', 'proposed', 'provided', 'published', 'purchased', 'qualified', 'quantified',
            'raised', 'ranked', 'rated', 'realized', 'recommended', 'reconciled', 'recorded', 'recruited', 'reduced',
            'referred', 'refined', 'regulated', 'rehabilitated', 'reinforced', 'rejected', 'remodeled', 'rendered',
            'reorganized', 'repaired', 'replaced', 'represented', 'researched', 'resolved', 'responded', 'restored',
            'restructured', 'retained', 'retrieved', 'reviewed', 'revised', 'saved', 'scheduled', 'screened', 'secured',
            'selected', 'served', 'serviced', 'shaped', 'simplified', 'solved', 'sorted', 'specified', 'specified',
            'spearheaded', 'standardized', 'streamlined', 'strengthened', 'structured', 'supervised', 'supplied',
            'supported', 'surveyed', 'systematized', 'targeted', 'taught', 'tested', 'trained', 'transformed',
            'translated', 'treated', 'triggered', 'troubleshooted', 'uncovered', 'understood', 'unified', 'updated',
            'upgraded', 'utilized', 'validated', 'verified', 'visualized', 'wrote'
        ]
        
        self.weak_phrases = [
            'responsible for', 'duties included', 'worked on', 'helped with', 'assisted in', 'participated in',
            'involved in', 'exposed to', 'familiar with', 'basic knowledge of', 'some experience with',
            'contributed to', 'supported the team', 'was in charge of', 'had to', 'needed to', 'tasked with'
        ]
        
        self.important_sections = ['summary', 'experience', 'education', 'skills', 'projects', 'certifications']

    def analyze_resume(self, resume_text, job_description=""):
        issues = []
        suggestions = []
        text_lower = resume_text.lower()
        
        # 1. Check for missing technical keywords (if job description provided)
        if job_description:
            job_keywords = self.extract_keywords_from_job_description(job_description)
            missing_from_job = []
            for keyword in job_keywords:
                if keyword.lower() not in text_lower:
                    missing_from_job.append(keyword)
            
            if missing_from_job:
                issues.append({
                    'type': 'missing_job_keywords',
                    'message': f'Missing keywords from job description: {", ".join(missing_from_job[:5])}',
                    'severity': 'high',
                    'suggestion': 'Include these keywords naturally in your experience or skills section.'
                })
        else:
            # Check for general missing technical skills
            missing_technical = []
            for skill in self.technical_skills[:20]:  # Check first 20 most common
                if skill.lower() not in text_lower:
                    missing_technical.append(skill)
            
            if len(missing_technical) > 15:  # If missing too many common skills
                issues.append({
                    'type': 'missing_technical_skills',
                    'message': f'Consider adding more technical skills like: {", ".join(missing_technical[:5])}',
                    'severity': 'medium',
                    'suggestion': 'Add relevant technical skills to your Skills section.'
                })

        # 2. Check for weak wording
        weak_phrases_found = []
        for phrase in self.weak_phrases:
            if phrase in text_lower:
                weak_phrases_found.append(phrase)
                issues.append({
                    'type': 'weak_wording',
                    'message': f'Weak phrase detected: "{phrase}"',
                    'severity': 'medium',
                    'suggestion': f'Replace with strong action verbs like: {", ".join(self.action_verbs[:3])}'
                })

        # 3. Check for missing important sections
        missing_sections = []
        for section in self.important_sections:
            if section not in text_lower:
                missing_sections.append(section)
        
        if 'experience' in missing_sections:
            issues.append({
                'type': 'missing_experience',
                'message': 'Experience section not found',
                'severity': 'high',
                'suggestion': 'Add a detailed work experience section with achievements.'
            })
        elif 'experience' not in missing_sections:
            # Check if experience section has quantifiable achievements
            experience_section = self.extract_section(resume_text, 'experience')
            if experience_section:
                if not self.has_quantifiable_achievements(experience_section):
                    issues.append({
                        'type': 'weak_experience',
                        'message': 'Experience lacks quantifiable achievements',
                        'severity': 'medium',
                        'suggestion': 'Add numbers and metrics to your achievements (e.g., "Increased sales by 25%")'
                    })

        if 'skills' in missing_sections:
            issues.append({
                'type': 'missing_skills',
                'message': 'Skills section not found',
                'severity': 'high',
                'suggestion': 'Add a dedicated skills section with relevant technical and soft skills.'
            })

        # 4. Check resume length and content quality
        word_count = len(resume_text.split())
        if word_count < 200:
            issues.append({
                'type': 'too_short',
                'message': 'Resume appears too short (less than 200 words)',
                'severity': 'medium',
                'suggestion': 'Expand your experience descriptions with more details and achievements.'
            })
        elif word_count > 1000:
            issues.append({
                'type': 'too_long',
                'message': 'Resume appears too long (more than 1000 words)',
                'severity': 'low',
                'suggestion': 'Consider condensing your resume to 1-2 pages maximum.'
            })

        # 5. Check for contact information
        if not self.has_contact_info(resume_text):
            issues.append({
                'type': 'missing_contact',
                'message': 'Contact information not detected',
                'severity': 'medium',
                'suggestion': 'Add your email, phone number, and LinkedIn profile at the top.'
            })

        return issues

    def extract_keywords_from_job_description(self, job_desc):
        # Simple keyword extraction - in real app, you'd use NLP
        words = re.findall(r'\b\w+\b', job_desc.lower())
        # Filter out common words and keep technical terms
        technical_words = [word for word in words if len(word) > 3 and word not in ['with', 'the', 'and', 'for', 'are', 'you']]
        return list(set(technical_words))[:10]  # Return unique keywords

    def extract_section(self, text, section_name):
        # Simple section extraction
        lines = text.split('\n')
        in_section = False
        section_content = []
        
        for line in lines:
            if section_name in line.lower():
                in_section = True
                continue
            elif in_section and any(header in line.lower() for header in ['education', 'skills', 'projects', 'certifications', 'summary']):
                break
            elif in_section:
                section_content.append(line)
        
        return ' '.join(section_content)

    def has_quantifiable_achievements(self, text):
        # Look for numbers, percentages, dollars, time periods
        patterns = [r'\d+%', r'\$\d+', r'\d+\s*(months|years|days|weeks)', r'\d+\s*(people|users|customers|clients)']
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False

    def has_contact_info(self, text):
        # Simple email and phone detection
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        
        return bool(re.search(email_pattern, text)) or bool(re.search(phone_pattern, text))

def analyze_resume_text(resume_text, job_description=""):
    analyzer = ATSAnalyzer()
    return analyzer.analyze_resume(resume_text, job_description)