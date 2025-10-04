import re

def analyze_resume_text(resume_text, job_description=""):
    """Analyze resume text dynamically and calculate ATS score"""
    issues = []
    base_score = 100
    
    # Debug: Print what we're analyzing
    print(f"🔍 Analyzing resume with {len(resume_text)} characters")
    
    # If extraction failed, return error
    if "ERROR: Could not extract text" in resume_text:
        issues.append({
            'type': 'extraction_error',
            'message': 'Could not read resume content. Please ensure your PDF/DOCX is not scanned or password protected.',
            'severity': 'high',
            'suggestion': 'Try converting your resume to a different format or ensure it contains selectable text.',
            'score_impact': -50
        })
        return issues, max(0, base_score - 50)
    
    if len(resume_text.strip()) < 50:
        issues.append({
            'type': 'empty_resume',
            'message': 'Resume appears to be empty or unreadable.',
            'severity': 'high',
            'suggestion': 'Please upload a resume with actual text content.',
            'score_impact': -40
        })
        return issues, max(0, base_score - 40)
    
    text_lower = resume_text.lower()
    score_deductions = 0
    
    # 1. Check for contact information (-5 points each missing)
    has_email = bool(re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text_lower))
    has_phone = bool(re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text_lower))
    
    if not has_email:
        issues.append({
            'type': 'missing_email',
            'message': 'Email address not found',
            'severity': 'medium',
            'suggestion': 'Add your professional email address at the top of your resume.',
            'score_impact': -5
        })
        score_deductions += 5
    
    if not has_phone:
        issues.append({
            'type': 'missing_phone',
            'message': 'Phone number not found',
            'severity': 'medium',
            'suggestion': 'Add your phone number for easy contact.',
            'score_impact': -5
        })
        score_deductions += 5
    
    # 2. Check for essential sections (-10 to -15 points each missing)
    essential_sections = {
        'experience': {
            'keywords': ['experience', 'work history', 'employment', 'professional experience'],
            'deduction': 15,
            'severity': 'high'
        },
        'education': {
            'keywords': ['education', 'academic', 'university', 'college', 'degree', 'bachelor', 'master'],
            'deduction': 10,
            'severity': 'high'
        },
        'skills': {
            'keywords': ['skills', 'technical skills', 'competencies', 'abilities', 'expertise'],
            'deduction': 12,
            'severity': 'high'
        }
    }
    
    for section, config in essential_sections.items():
        found = False
        for keyword in config['keywords']:
            if keyword in text_lower:
                found = True
                break
        
        if not found:
            issues.append({
                'type': f'missing_{section}',
                'message': f'{section.title()} section not detected',
                'severity': config['severity'],
                'suggestion': f'Add a dedicated {section} section with relevant details.',
                'score_impact': -config['deduction']
            })
            score_deductions += config['deduction']
    
    # 3. Check for action verbs vs weak phrases (-8 points for weak language)
    strong_verbs = [
        'achieved', 'built', 'created', 'developed', 'designed', 'implemented', 
        'increased', 'improved', 'led', 'managed', 'optimized', 'reduced', 'spearheaded',
        'accelerated', 'accomplished', 'analyzed', 'boosted', 'delivered', 'enhanced',
        'established', 'executed', 'generated', 'launched', 'produced', 'resolved',
        'streamlined', 'transformed'
    ]
    
    weak_phrases = [
        'responsible for', 'duties included', 'worked on', 'helped with', 
        'assisted in', 'participated in', 'involved in', 'familiar with',
        'basic knowledge', 'some experience', 'exposed to'
    ]
    
    # Count strong verbs
    strong_verb_count = 0
    for verb in strong_verbs:
        strong_verb_count += text_lower.count(verb)
    
    # Check for weak phrases
    weak_found = []
    for phrase in weak_phrases:
        if phrase in text_lower:
            weak_found.append(phrase)
    
    if weak_found:
        issues.append({
            'type': 'weak_wording',
            'message': f'Weak phrases detected: {", ".join(weak_found[:3])}',
            'severity': 'medium',
            'suggestion': f'Replace weak phrases with strong action verbs like: {", ".join(strong_verbs[:4])}',
            'score_impact': -8
        })
        score_deductions += 8
    elif strong_verb_count == 0 and ('experience' in text_lower or 'work' in text_lower):
        issues.append({
            'type': 'passive_language',
            'message': 'Resume lacks strong action verbs',
            'severity': 'medium',
            'suggestion': f'Start bullet points with powerful action verbs like: {", ".join(strong_verbs[:4])}',
            'score_impact': -6
        })
        score_deductions += 6
    
    # 4. Check for quantifiable achievements (-7 points if missing)
    has_numbers = (bool(re.search(r'\d+[%$]', text_lower)) or 
                   bool(re.search(r'\d+\s*(months|years|people|users|customers|clients|projects|team|revenue|sales|cost|time|efficiency)', text_lower)))
    
    if not has_numbers and ('experience' in text_lower or 'work' in text_lower):
        issues.append({
            'type': 'lacks_metrics',
            'message': 'Experience lacks quantifiable achievements',
            'severity': 'medium',
            'suggestion': 'Add specific numbers and metrics to demonstrate impact (e.g., "Increased sales by 25%" or "Managed a team of 5 developers").',
            'score_impact': -7
        })
        score_deductions += 7
    
    # 5. Job description matching (-10 points for missing key requirements)
    if job_description.strip():
        job_lower = job_description.lower()
        job_keywords = extract_keywords_from_text(job_lower)
        resume_keywords = extract_keywords_from_text(text_lower)
        
        missing_from_job = []
        for keyword in job_keywords:
            if keyword not in resume_keywords and len(keyword) > 2:
                missing_from_job.append(keyword)
        
        if missing_from_job:
            deduction = min(len(missing_from_job) * 3, 15)  # Max 15 points deduction
            issues.append({
                'type': 'missing_job_keywords',
                'message': f'Missing keywords from job description: {", ".join(missing_from_job[:5])}',
                'severity': 'high',
                'suggestion': f'Incorporate these job-specific keywords naturally into your experience or skills section to pass ATS screening.',
                'score_impact': -deduction
            })
            score_deductions += deduction
    
    # 6. Check resume length (-5 points if too short or too long)
    word_count = len(resume_text.split())
    if word_count < 150:
        issues.append({
            'type': 'too_short',
            'message': f'Resume is very short ({word_count} words)',
            'severity': 'low',
            'suggestion': 'Expand your experience descriptions with more details, achievements, and relevant skills.',
            'score_impact': -5
        })
        score_deductions += 5
    elif word_count > 1000:
        issues.append({
            'type': 'too_long',
            'message': f'Resume is quite long ({word_count} words)',
            'severity': 'low',
            'suggestion': 'Condense your resume to 1-2 pages maximum. Focus on recent and relevant experience.',
            'score_impact': -5
        })
        score_deductions += 5
    
    # Calculate final score
    final_score = max(0, base_score - score_deductions)
    
    # Add positive feedback if score is high
    if final_score >= 85 and not issues:
        issues.append({
            'type': 'excellent_resume',
            'message': 'Excellent ATS-friendly resume!',
            'severity': 'positive',
            'suggestion': 'Your resume is well-structured and optimized for applicant tracking systems.',
            'score_impact': 0
        })
    
    # Debug: Print number of issues found
    print(f"✅ Found {len(issues)} issues, final score: {final_score}")
    
    return issues, final_score

def extract_keywords_from_text(text):
    """Extract potential keywords from text"""
    # Simple keyword extraction - remove common words
    common_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their', 'mine', 'yours', 'hers', 'ours', 'theirs'}
    
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    keywords = [word for word in words if word not in common_words]
    return list(set(keywords))