class ResumeTemplate:
    def __init__(self):
        self.templates = {
            1: self.template_professional,
            2: self.template_modern,
            3: self.template_creative,
            4: self.template_minimalist,
            5: self.template_executive
        }
    
    def get_template(self, template_id, resume_data):
        """Get resume template by ID"""
        template_func = self.templates.get(template_id, self.template_professional)
        return template_func(resume_data)
    
    def template_professional(self, data):
        """Professional template - ATS friendly, single column"""
        html = f'''
        <div class="resume professional">
            <div class="header">
                <h1>{data.get('full_name', '')}</h1>
                <h2>{data.get('professional_title', '')}</h2>
                <div class="contact-info">
                    <span>{data.get('email', '')}</span> | 
                    <span>{data.get('phone', '')}</span> |
                    <span>{data.get('linkedin', '')}</span>
                </div>
            </div>
            
            <div class="section">
                <h3>Professional Summary</h3>
                <p>{data.get('career_objective', '')}</p>
            </div>
            
            <div class="section">
                <h3>Skills</h3>
                <div class="skills-list">
                    <p><strong>Technical:</strong> {', '.join(data.get('technical_skills', []))}</p>
                    <p><strong>Soft Skills:</strong> {', '.join(data.get('soft_skills', []))}</p>
                    <p><strong>Tools:</strong> {', '.join(data.get('tools', []))}</p>
                </div>
            </div>
            
            <div class="section">
                <h3>Experience</h3>
                {self.render_experience(data.get('experience', []))}
            </div>
            
            <div class="section">
                <h3>Education</h3>
                {self.render_education(data.get('education', []))}
            </div>
            
            <div class="section">
                <h3>Projects</h3>
                {self.render_projects(data.get('projects', []))}
            </div>
        </div>
        '''
        return html
    
    def template_modern(self, data):
        """Modern template - Two column layout"""
        html = f'''
        <div class="resume modern">
            <div class="row">
                <div class="col-left">
                    <div class="profile-image">
                        <img src="{data.get('profile_image', '/static/default-avatar.png')}" alt="Profile">
                    </div>
                    <h1>{data.get('full_name', '')}</h1>
                    <h2>{data.get('professional_title', '')}</h2>
                    
                    <div class="contact-section">
                        <h3>Contact</h3>
                        <p>📧 {data.get('email', '')}</p>
                        <p>📱 {data.get('phone', '')}</p>
                        <p>🔗 {data.get('linkedin', '')}</p>
                    </div>
                    
                    <div class="skills-section">
                        <h3>Skills</h3>
                        <div class="skill-tags">
                            {self.render_skill_tags(data.get('technical_skills', []))}
                        </div>
                    </div>
                </div>
                
                <div class="col-right">
                    <div class="section">
                        <h3>Professional Summary</h3>
                        <p>{data.get('career_objective', '')}</p>
                    </div>
                    
                    <div class="section">
                        <h3>Experience</h3>
                        {self.render_experience_modern(data.get('experience', []))}
                    </div>
                    
                    <div class="section">
                        <h3>Education</h3>
                        {self.render_education(data.get('education', []))}
                    </div>
                    
                    <div class="section">
                        <h3>Projects</h3>
                        {self.render_projects(data.get('projects', []))}
                    </div>
                </div>
            </div>
        </div>
        '''
        return html
    
    def template_creative(self, data):
        """Creative template - Colorful design"""
        colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12']
        html = f'''
        <div class="resume creative">
            <div class="header" style="background: linear-gradient(135deg, {colors[0]}, {colors[1]});">
                <div class="header-content">
                    <h1>{data.get('full_name', '')}</h1>
                    <h2>{data.get('professional_title', '')}</h2>
                    <div class="contact-info">
                        <span>{data.get('email', '')}</span>
                        <span>{data.get('phone', '')}</span>
                    </div>
                </div>
            </div>
            
            <div class="content-grid">
                <div class="left-panel" style="border-color: {colors[2]};">
                    <div class="section">
                        <h3 style="color: {colors[2]};">Profile</h3>
                        <p>{data.get('career_objective', '')}</p>
                    </div>
                    
                    <div class="section">
                        <h3 style="color: {colors[2]};">Skills</h3>
                        {self.render_creative_skills(data)}
                    </div>
                </div>
                
                <div class="right-panel" style="border-color: {colors[3]};">
                    <div class="section">
                        <h3 style="color: {colors[3]};">Experience</h3>
                        {self.render_creative_experience(data.get('experience', []))}
                    </div>
                    
                    <div class="section">
                        <h3 style="color: {colors[3]};">Education</h3>
                        {self.render_creative_education(data.get('education', []))}
                    </div>
                </div>
            </div>
        </div>
        '''
        return html
    
    def template_minimalist(self, data):
        """Minimalist template - Clean and simple"""
        html = f'''
        <div class="resume minimalist">
            <div class="container">
                <h1 class="name">{data.get('full_name', '')}</h1>
                <h2 class="title">{data.get('professional_title', '')}</h2>
                
                <div class="contact-line">
                    {data.get('email', '')} • {data.get('phone', '')} • {data.get('linkedin', '')}
                </div>
                
                <div class="summary">
                    <h3>Summary</h3>
                    <p>{data.get('career_objective', '')}</p>
                </div>
                
                <div class="skills-minimal">
                    <h3>Core Competencies</h3>
                    {self.render_minimal_skills(data.get('technical_skills', []))}
                </div>
                
                <div class="experience-minimal">
                    <h3>Professional Experience</h3>
                    {self.render_minimal_experience(data.get('experience', []))}
                </div>
                
                <div class="education-minimal">
                    <h3>Education</h3>
                    {self.render_minimal_education(data.get('education', []))}
                </div>
            </div>
        </div>
        '''
        return html
    
    def template_executive(self, data):
        """Executive template - Corporate style"""
        html = f'''
        <div class="resume executive">
            <div class="executive-header">
                <div class="name-title">
                    <h1>{data.get('full_name', '')}</h1>
                    <h2>{data.get('professional_title', '')}</h2>
                </div>
                <div class="executive-contact">
                    <p>{data.get('email', '')}</p>
                    <p>{data.get('phone', '')}</p>
                    <p>{data.get('linkedin', '')}</p>
                </div>
            </div>
            
            <div class="executive-summary">
                <h3>Executive Summary</h3>
                <p>{data.get('career_objective', '')}</p>
            </div>
            
            <div class="executive-grid">
                <div class="executive-left">
                    <h3>Core Qualifications</h3>
                    {self.render_executive_skills(data)}
                    
                    <h3>Education</h3>
                    {self.render_executive_education(data.get('education', []))}
                </div>
                
                <div class="executive-right">
                    <h3>Professional Experience</h3>
                    {self.render_executive_experience(data.get('experience', []))}
                    
                    <h3>Key Achievements</h3>
                    {self.render_executive_achievements(data.get('achievements', []))}
                </div>
            </div>
        </div>
        '''
        return html
    
    # Helper methods
    def render_experience(self, experiences):
        if not experiences:
            return "<p>No experience listed</p>"
        html = ""
        for exp in experiences:
            html += f'''
            <div class="experience-item">
                <h4>{exp.get('job_role', '')} at {exp.get('company_name', '')}</h4>
                <p class="duration">{exp.get('duration', '')}</p>
                <p>{exp.get('achievements', '')}</p>
            </div>
            '''
        return html
    
    def render_education(self, education):
        if not education:
            return "<p>No education listed</p>"
        html = ""
        for edu in education:
            html += f'''
            <div class="education-item">
                <h4>{edu.get('degree', '')}</h4>
                <p>{edu.get('institution', '')} | {edu.get('graduation_year', '')}</p>
                <p>CGPA: {edu.get('cgpa', '')}</p>
            </div>
            '''
        return html
    
    def render_projects(self, projects):
        if not projects:
            return "<p>No projects listed</p>"
        html = ""
        for proj in projects:
            html += f'''
            <div class="project-item">
                <h4>{proj.get('project_title', '')}</h4>
                <p>{proj.get('description', '')}</p>
                <p><strong>Technologies:</strong> {proj.get('technologies', '')}</p>
            </div>
            '''
        return html
    
    def render_skill_tags(self, skills):
        if not skills:
            return ""
        html = ""
        for skill in skills:
            html += f'<span class="skill-tag">{skill}</span>'
        return html
    
    def render_experience_modern(self, experiences):
        if not experiences:
            return "<p>No experience listed</p>"
        html = ""
        for exp in experiences:
            html += f'''
            <div class="experience-modern">
                <div class="exp-header">
                    <strong>{exp.get('job_role', '')}</strong> at {exp.get('company_name', '')}
                    <span class="exp-date">{exp.get('duration', '')}</span>
                </div>
                <p>{exp.get('achievements', '')}</p>
            </div>
            '''
        return html
    
    def render_creative_skills(self, data):
        skills = {
            'Technical': data.get('technical_skills', []),
            'Soft': data.get('soft_skills', []),
            'Tools': data.get('tools', [])
        }
        html = ""
        for category, skill_list in skills.items():
            if skill_list:
                html += f"<p><strong>{category}:</strong> {', '.join(skill_list)}</p>"
        return html
    
    def render_creative_experience(self, experiences):
        if not experiences:
            return "<p>No experience listed</p>"
        html = ""
        for exp in experiences:
            html += f'''
            <div class="creative-exp">
                <h4>{exp.get('job_role', '')}</h4>
                <h5>{exp.get('company_name', '')} | {exp.get('duration', '')}</h5>
                <p>{exp.get('achievements', '')}</p>
            </div>
            '''
        return html
    
    def render_creative_education(self, education):
        if not education:
            return "<p>No education listed</p>"
        html = ""
        for edu in education:
            html += f'''
            <div class="creative-edu">
                <h4>{edu.get('degree', '')}</h4>
                <p>{edu.get('institution', '')} - {edu.get('graduation_year', '')}</p>
            </div>
            '''
        return html
    
    def render_minimal_skills(self, skills):
        if not skills:
            return ""
        return ", ".join(skills)
    
    def render_minimal_experience(self, experiences):
        if not experiences:
            return "<p>No experience listed</p>"
        html = ""
        for exp in experiences:
            html += f'''
            <div class="minimal-exp">
                <p><strong>{exp.get('job_role', '')}</strong> at {exp.get('company_name', '')}</p>
                <p class="minimal-date">{exp.get('duration', '')}</p>
                <p>{exp.get('achievements', '')}</p>
            </div>
            '''
        return html
    
    def render_minimal_education(self, education):
        if not education:
            return "<p>No education listed</p>"
        html = ""
        for edu in education:
            html += f'''
            <div class="minimal-edu">
                <p><strong>{edu.get('degree', '')}</strong> - {edu.get('institution', '')}</p>
                <p class="minimal-date">{edu.get('graduation_year', '')}</p>
            </div>
            '''
        return html
    
    def render_executive_skills(self, data):
        skills = []
        if data.get('technical_skills'):
            skills.extend(data['technical_skills'][:5])
        if data.get('soft_skills'):
            skills.extend(data['soft_skills'][:3])
        
        if not skills:
            return "<p>No skills listed</p>"
        
        html = "<ul>"
        for skill in skills:
            html += f"<li>{skill}</li>"
        html += "</ul>"
        return html
    
    def render_executive_education(self, education):
        if not education:
            return "<p>No education listed</p>"
        html = ""
        for edu in education[:2]:
            html += f'''
            <div class="executive-edu">
                <p><strong>{edu.get('degree', '')}</strong></p>
                <p>{edu.get('institution', '')} | {edu.get('graduation_year', '')}</p>
            </div>
            '''
        return html
    
    def render_executive_experience(self, experiences):
        if not experiences:
            return "<p>No experience listed</p>"
        html = ""
        for exp in experiences[:3]:
            html += f'''
            <div class="executive-exp">
                <p><strong>{exp.get('job_role', '')}</strong> | {exp.get('company_name', '')}</p>
                <p class="executive-date">{exp.get('duration', '')}</p>
                <p>{exp.get('achievements', '')[:150]}...</p>
            </div>
            '''
        return html
    
    def render_executive_achievements(self, achievements):
        if not achievements:
            return "<p>No achievements listed</p>"
        html = "<ul>"
        for achievement in achievements[:3]:
            html += f"<li>{achievement}</li>"
        html += "</ul>"
        return html