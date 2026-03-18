from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
import os

class PDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.HexColor('#2c3e50')
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceBefore=20,
            spaceAfter=10,
            textColor=colors.HexColor('#3498db')
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=8,
            leading=14
        ))
        
        self.styles.add(ParagraphStyle(
            name='ContactInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#7f8c8d'),
            alignment=1  # Center alignment
        ))
    
    def generate_pdf(self, resume_data, template_id=1):
        """Generate PDF resume"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4,
                               rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=72)
        
        story = []
        
        # Add profile image if exists
        if resume_data.get('profile_image'):
            try:
                img_path = resume_data['profile_image'].lstrip('/')
                if os.path.exists(img_path):
                    img = Image(img_path, width=1.5*inch, height=1.5*inch)
                    story.append(img)
                    story.append(Spacer(1, 12))
            except:
                pass
        
        # Add name and title
        story.append(Paragraph(resume_data.get('full_name', ''), self.styles['CustomTitle']))
        story.append(Paragraph(resume_data.get('professional_title', ''), self.styles['Heading2']))
        story.append(Spacer(1, 12))
        
        # Contact information
        contact_info = f"""
        {resume_data.get('email', '')} | {resume_data.get('phone', '')} | 
        {resume_data.get('linkedin', '')}
        """
        story.append(Paragraph(contact_info, self.styles['ContactInfo']))
        story.append(Spacer(1, 20))
        
        # Professional Summary
        if resume_data.get('career_objective'):
            story.append(Paragraph('Professional Summary', self.styles['CustomHeading']))
            story.append(Paragraph(resume_data['career_objective'], self.styles['CustomBody']))
            story.append(Spacer(1, 12))
        
        # Skills
        skills_data = []
        if resume_data.get('technical_skills'):
            skills_data.append(['Technical Skills', ', '.join(resume_data['technical_skills'])])
        if resume_data.get('soft_skills'):
            skills_data.append(['Soft Skills', ', '.join(resume_data['soft_skills'])])
        if resume_data.get('tools'):
            skills_data.append(['Tools', ', '.join(resume_data['tools'])])
        
        if skills_data:
            story.append(Paragraph('Skills', self.styles['CustomHeading']))
            skills_table = Table(skills_data, colWidths=[2*inch, 4*inch])
            skills_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey)
            ]))
            story.append(skills_table)
            story.append(Spacer(1, 12))
        
        # Experience
        if resume_data.get('experience'):
            story.append(Paragraph('Professional Experience', self.styles['CustomHeading']))
            for exp in resume_data['experience']:
                exp_text = f"""
                <b>{exp.get('job_role', '')}</b> at <b>{exp.get('company_name', '')}</b><br/>
                <i>{exp.get('duration', '')}</i><br/>
                {exp.get('achievements', '')}
                """
                story.append(Paragraph(exp_text, self.styles['CustomBody']))
                story.append(Spacer(1, 8))
        
        # Education
        if resume_data.get('education'):
            story.append(Paragraph('Education', self.styles['CustomHeading']))
            edu_data = [['Degree', 'Institution', 'Year', 'CGPA']]
            for edu in resume_data['education']:
                edu_data.append([
                    edu.get('degree', ''),
                    edu.get('institution', ''),
                    str(edu.get('graduation_year', '')),
                    str(edu.get('cgpa', ''))
                ])
            
            edu_table = Table(edu_data, colWidths=[1.5*inch, 2*inch, 1*inch, 1*inch])
            edu_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('ALIGN', (2, 0), (3, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey)
            ]))
            story.append(edu_table)
            story.append(Spacer(1, 12))
        
        # Projects
        if resume_data.get('projects'):
            story.append(Paragraph('Projects', self.styles['CustomHeading']))
            for proj in resume_data['projects']:
                proj_text = f"""
                <b>{proj.get('project_title', '')}</b><br/>
                {proj.get('description', '')}<br/>
                <i>Technologies: {proj.get('technologies', '')}</i>
                """
                story.append(Paragraph(proj_text, self.styles['CustomBody']))
                story.append(Spacer(1, 8))
        
        # Additional sections
        if resume_data.get('certifications'):
            story.append(Paragraph('Certifications', self.styles['CustomHeading']))
            cert_text = ', '.join(resume_data['certifications'])
            story.append(Paragraph(cert_text, self.styles['CustomBody']))
            story.append(Spacer(1, 8))
        
        if resume_data.get('languages'):
            story.append(Paragraph('Languages', self.styles['CustomHeading']))
            lang_text = ', '.join(resume_data['languages'])
            story.append(Paragraph(lang_text, self.styles['CustomBody']))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def generate_ats_friendly_pdf(self, resume_data):
        """Generate ATS-friendly PDF with simple formatting"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4,
                               rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=72)
        
        story = []
        
        # Simple ATS-friendly format
        story.append(Paragraph(resume_data.get('full_name', '').upper(), self.styles['Title']))
        story.append(Spacer(1, 12))
        
        # Contact info in simple format
        contact = f"Email: {resume_data.get('email', '')} | Phone: {resume_data.get('phone', '')}"
        story.append(Paragraph(contact, self.styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Sections with simple headings
        sections = [
            ('SUMMARY', 'career_objective'),
            ('SKILLS', self._format_skills),
            ('EXPERIENCE', self._format_experience_simple),
            ('EDUCATION', self._format_education_simple),
            ('PROJECTS', self._format_projects_simple)
        ]
        
        for title, field in sections:
            story.append(Paragraph(title, self.styles['Heading2']))
            story.append(Spacer(1, 6))
            
            if callable(field):
                content = field(resume_data)
            else:
                content = resume_data.get(field, '')
            
            if content:
                story.append(Paragraph(str(content), self.styles['Normal']))
            story.append(Spacer(1, 12))
        
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def _format_skills(self, data):
        """Format skills for ATS-friendly PDF"""
        skills = []
        if data.get('technical_skills'):
            skills.extend(data['technical_skills'])
        if data.get('soft_skills'):
            skills.extend(data['soft_skills'])
        if data.get('tools'):
            skills.extend(data['tools'])
        return ', '.join(skills)
    
    def _format_experience_simple(self, data):
        """Format experience for ATS-friendly PDF"""
        if not data.get('experience'):
            return ""
        
        exp_text = ""
        for exp in data['experience']:
            exp_text += f"{exp.get('job_role', '')} at {exp.get('company_name', '')}\n"
            exp_text += f"Duration: {exp.get('duration', '')}\n"
            exp_text += f"{exp.get('achievements', '')}\n\n"
        return exp_text
    
    def _format_education_simple(self, data):
        """Format education for ATS-friendly PDF"""
        if not data.get('education'):
            return ""
        
        edu_text = ""
        for edu in data['education']:
            edu_text += f"{edu.get('degree', '')} - {edu.get('institution', '')}\n"
            edu_text += f"Graduation: {edu.get('graduation_year', '')}, CGPA: {edu.get('cgpa', '')}\n\n"
        return edu_text
    
    def _format_projects_simple(self, data):
        """Format projects for ATS-friendly PDF"""
        if not data.get('projects'):
            return ""
        
        proj_text = ""
        for proj in data['projects']:
            proj_text += f"{proj.get('project_title', '')}\n"
            proj_text += f"{proj.get('description', '')}\n"
            proj_text += f"Technologies: {proj.get('technologies', '')}\n\n"
        return proj_text