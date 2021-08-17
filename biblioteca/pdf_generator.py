from flask import current_app as app
from os import path

from fpdf import FPDF
from datetime import datetime

PDF_W=210
PDF_H=297
MARGIN=25.0

class TermoCompromisso(FPDF):
    def create(self, title, txt):
        self.add_page()
        self.borda()
        self.imagex()
        self.titles(title)
        self.texts(txt)
        
    def borda(self):
        self.set_line_width(0.0)
        self.rect(5.0, 5.0, 200.0,287.0)
        
    def imagex(self):
        self.set_xy(40,20.0)
        
        self.image(
            path.join(app.config['STATIC_FOLDER'], 'logos', 'logo-cps-escuro.png'),  
            link='', type='', w=400/8, h=150/8
        )
        self.set_xy(120,20.0)
        self.image(
            path.join(app.config['STATIC_FOLDER'], 'logos', 'logo-fatec-2.jpg'),  
            link='', type='', w=400/8, h=150/8
        )
    
    def titles(self, title):
        self.set_xy(0.0, PDF_H/8)
        self.set_font('Arial', 'B', 14)
        self.set_text_color(0, 0, 0)
        self.cell(w=PDF_W, h=40.0, align='C', txt=title, border=0)

    def texts(self, txt):
        self.set_xy(MARGIN, 70.0)
        self.set_right_margin(MARGIN)
        self.set_text_color(0, 0, 0)
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 6, txt)
        
        self.set_xy((PDF_W/5) * 3, 180.0)
        self.multi_cell(
            w=0, 
            h=6,
            txt="Carapicuíba, {0}\nHora: {1}".format(
                datetime.now().strftime('%d/%m/%Y'), 
                datetime.now().strftime('%H:%M')
            ), 
            align="R")

