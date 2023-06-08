import pygame
import random
import time
from sudoku_generator import *

class SudokuGame:

    def __init__(self,grille,solution):
       
        if not grille:
           grille = [[0] * 9 for _ in range(9)]
        
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 900))
        pygame.display.set_caption("Sudoku Game")

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)

        self.font = pygame.font.Font(None, 46)
        self.font_candidate = pygame.font.Font(None,25)
        self.font_menu = pygame.font.Font(None,25)

        self.cell_size = 90
        self.cell_margin = 0
        self.grid_margin = 40

        self.menu_open = False  # Variable pour indiquer si le menu est ouvert
        self.hovered_option = None  # Variable pour suivre l'option survolée par la souris


        self.grid = grille
        self.solution=solution
        self.menu_option_rects = []  # Rectangles des options de menu
        self.selected_cell = None


        self.menu_option_rects = []  # Rectangles des options de menu
        self.create_widgets()
        self.create_menu()
        
        self.initial_color=pygame.Color(random.randint(190,220),random.randint(190,220),random.randint(190,220))
        self.completed_color=pygame.Color(random.randint(220,250),random.randint(220,250),random.randint(220,250))

        self.textbox_rect=None
        self.input_text = ""                    
        self.candidate_mode = False
     
        self.pause_button_hovered=False
        self.start_time=time.time()
        self.paused_time = 0
        self.duration_heures=0
        self.duration_minutes=0
        self.duration_secondes=0 
        
    
    def create_menu(self):
        self.menu_button = pygame.Rect(1100, 20, 40, 40)  # Position et taille du bouton de menu
        self.menu_options = [
            {'text': 'Nouvelle partie', 'action': self.start_new_game},
            {'text': 'Réinitialiser grille', 'action': self.reinitialize_grid},
            {'text': 'Résoudre grille','action':self.solve_grid},
            {'text': 'Quitter', 'action': quit}
         ]  # Options de menu avec leur texte et action associée
        self.menu_option_rects = []  # Liste de rectangles pour les options de menu
    
    def create_menu_options(self):
        self.menu_option_rects = []  # Réinitialiser la liste des rectangles des options de menu
        menu_top = self.grid_margin + 60
        menu_left = self.screen.get_width() - self.grid_margin - 200 
        for index, option in enumerate(self.menu_options):
            option_rect = pygame.Rect(menu_left,menu_top + index * 60,200,50)
            self.menu_option_rects.append(option_rect)
    
    def draw_timer(self):

        timer_top = self.grid_margin 
        timer_left = self.screen.get_width() - self.grid_margin - 200 
        timer_rect = pygame.Rect(timer_left,timer_top,80,40)
        
        pygame.draw.rect(self.screen,self.completed_color,timer_rect)
        str_time= str(self.duration_minutes+100)[-2:]+":"+str(self.duration_secondes+100)[-2:]
        text = self.font_menu.render(str_time,True,pygame.Color('black'))
        text_rect = text.get_rect(center=timer_rect.center)
        self.screen.blit(text, text_rect)

    
    def draw_pause_button(self):
        
        if self.pause_button['hovered']:
            color = self.initial_color
        else:
            color = self.completed_color
    
        pygame.draw.rect(self.screen,color,self.pause_button['rect'])
        pygame.draw.rect(self.screen,self.completed_color,self.pause_button['rect'],4)
        if self.pause_button['on_pause']:
            pygame.draw.polygon(self.screen, pygame.Color('black'), [(self.pause_button['left'] + 15, self.pause_button['top'] + 10), (self.pause_button['left'] + 15, self.pause_button['top'] + 30), (self.pause_button['left'] + 30, self.pause_button['top']  + 20)])
        else:
            pygame.draw.line(self.screen, pygame.Color('black'), (self.pause_button['left']+16,self.pause_button['top']+12), (self.pause_button['left']+16, self.pause_button['top']+28), 5)
            pygame.draw.line(self.screen, pygame.Color('black'), (self.pause_button['left']+24,self.pause_button['top']+12), (self.pause_button['left']+24, self.pause_button['top']+28), 5)
            
    
    def draw_menu_button(self):
        pygame.draw.rect(self.screen, pygame.Color('white'), self.menu_button)
        pygame.draw.line(self.screen, pygame.Color('black'), (1115, 40), (1140, 40), 4)
        pygame.draw.line(self.screen, pygame.Color('black'), (1115, 45), (1140, 45), 4)
        pygame.draw.line(self.screen, pygame.Color('black'), (1115, 50), (1140, 50), 4)

    def draw_menu_options(self):
        for index, option_rect in enumerate(self.menu_option_rects):
            if index==self.hovered_option:
                color = self.initial_color
            else:
                color = self.completed_color
            pygame.draw.rect(self.screen, color, option_rect)
            pygame.draw.rect(self.screen, pygame.Color('black'), option_rect, 2)
            text = self.font_menu.render(self.menu_options[index]['text'], True, pygame.Color('black'))
            text_rect = text.get_rect(center=option_rect.center)
            self.screen.blit(text, text_rect)
            
    def handle_menu_click(self, pos):
   
        if self.menu_button.collidepoint(pos):
            self.menu_open = not self.menu_open
            if self.menu_open:
                self.create_menu_options()

        if self.menu_open:
            for index, option_rect in enumerate(self.menu_option_rects):
                if option_rect.collidepoint(pos):
                    self.hovered_option = index  # Mettre à jour l'option survolée
                    self.menu_options[index]['action']()
                else:
                    self.hovered_option = None
        
        else:
             self.hovered_option = None
    
    def handle_pause_button(self,pos):
        if self.pause_button['rect'].collidepoint(pos):
            self.pause_button['hovered'] = True
            self.pause_button['on_pause'] = not self.pause_button['on_pause']
            if self.pause_button['on_pause']:
                self.pause_button['start_time'] = time.time()
            else:
                self.paused_time = self.paused_time + self.pause_button['duration']
                self.pause_button['duration']=0
        else:
            self.pause_button['hovered'] = False
        self.draw_pause_button()

    def draw_window(self):
        if self.pause_button['on_pause']:
           self.draw_pause_window()
        else:
            self.draw_grid()  # Dessiner la grille
        self.draw_menu_button()  #dessiner bouton hamburger du menu
        self.draw_timer() #dessiner le timer
        if not self.grid_completed():
            self.draw_pause_button() #dessiner le bouton pause
        
        if self.menu_open:
            pos = pygame.mouse.get_pos()
            for index, option_rect in enumerate(self.menu_option_rects):
                if option_rect.collidepoint(pos):
                    self.hovered_option = index  # Mettre à jour l'option survolée
            self.draw_menu_options()  # Dessiner les options de menu
        
        pygame.display.flip()
    
    def create_widgets(self):
        # create grid cells
        self.cells = [{'rect': pygame.Rect(self.grid_margin + j * (self.cell_size + self.cell_margin),
                                   self.grid_margin+i * (self.cell_size + self.cell_margin),
                                   self.cell_size, self.cell_size),
               'value': self.grid[i][j],
               'row': i,
               'col': j,
               'editable': self.grid[i][j] == 0,
               'candidate': ""}
              for i in range(9) for j in range(9)]
        
        # create the selected cell rectangle
        self.selected_rect = pygame.Rect(0, 0, self.cell_size, self.cell_size)
        self.selected_rect_color = pygame.Color('blue')

        # create pause button
        pause_top = self.grid_margin 
        pause_left = self.screen.get_width() - self.grid_margin - 120 
        self.pause_button = {'rect':pygame.Rect(pause_left,pause_top,40,40),'hovered':False,'top':pause_top,'left':pause_left,'on_pause':False,'start_time':None,'duration':0}
    
    def draw_pause_window(self):
        # draw the pause window
        w = 9 * (self.cell_size + self.cell_margin)
        rect = pygame.Rect(self.grid_margin,self.grid_margin,w,w)
        pygame.draw.rect(self.screen,pygame.Color("lightgray"),rect)
        
        text = self.font.render("En pause", True, pygame.Color('darkgray'))
        text_rect = text.get_rect(center=rect.center)
        self.screen.blit(text, text_rect)   
        
    
    def draw_grid(self):
        
        # Create a new display surface with the desired width and height
        thickness=4
        self.screen.fill(pygame.Color(self.WHITE))
        
        #initialize current grid to use the valid function of the sudoku generator module
        current_grid = [[0 for _ in range(9)] for _ in range(9)]
        for cell in self.cells:
            current_grid[cell["row"]][cell["col"]] = cell['value']

        #initialize color scheme
        
        if self.grid_completed():
            editable_color = self.completed_color
            non_editable_color = self.completed_color
        else:
            editable_color=self.completed_color
            non_editable_color=self.initial_color

        for cell in self.cells:
            row = cell["row"]
            col = cell["col"]
            value = cell["value"]
            pos = (row,col)
            
            text_color = 'black'
            if value !=0:
                if not valid(current_grid,value,pos):
                    text_color = 'red'
            
            if not cell['editable']:
                pygame.draw.rect(self.screen, pygame.Color(non_editable_color), cell['rect'])
            else:
                 pygame.draw.rect(self.screen, pygame.Color(editable_color), cell['rect']) 
            
            pygame.draw.rect(self.screen, pygame.Color('lightblue'), cell['rect'],1)
     
            if cell['value'] != 0:
                text = self.font.render(str(cell['value']), True, pygame.Color(text_color))
                text_rect = text.get_rect(center=cell['rect'].center)
                self.screen.blit(text, text_rect)
            else:
                text = self.font_candidate.render(str(cell['candidate']), True, pygame.Color(text_color))
                text_rect = text.get_rect(center=cell['rect'].center)
                self.screen.blit(text, text_rect)

            
            # Add thicker borders for 3x3 regions
            if (cell['row']) % 3 == 0 and (cell['col']) % 3 == 0:
                pygame.draw.line(self.screen, pygame.Color('black'), cell['rect'].topleft, cell['rect'].topright, thickness)
                pygame.draw.line(self.screen, pygame.Color('black'), cell['rect'].topleft, cell['rect'].bottomleft, thickness)
            elif (cell['row']) % 3 == 0:
                pygame.draw.line(self.screen, pygame.Color('black'), cell['rect'].topleft, cell['rect'].topright, thickness)
            elif (cell['col']) % 3 == 0:
                pygame.draw.line(self.screen, pygame.Color('black'), cell['rect'].topleft, cell['rect'].bottomleft, thickness)
            
            if (cell['row']) == 8:
                pygame.draw.line(self.screen, pygame.Color('black'), cell['rect'].bottomleft, cell['rect'].bottomright, thickness)
            if (cell['col']) == 8:
                pygame.draw.line(self.screen, pygame.Color('black'), cell['rect'].topright, cell['rect'].bottomright, thickness)

         
            if self.selected_cell:
                pygame.draw.rect(self.screen, self.selected_rect_color, self.selected_rect, thickness)
            
            if self.candidate_mode:
                    pygame.draw.rect(self.screen, pygame.Color('white'), self.textbox_rect)
                    pygame.draw.rect(self.screen, pygame.Color('red'), self.textbox_rect,4)
                    text = self.font_candidate.render(self.selected_cell['candidate'], True, pygame.Color('black'))
                    text_rect = text.get_rect(center=self.textbox_rect.center)
                    self.screen.blit(text, text_rect)
    
    def select_cell(self, cell):
        # initialize the selected cell
        self.selected_cell = cell
        self.selected_rect.topleft = cell['rect'].topleft
    
    def update_candidate(self):
        # update the list of candidate based on the input of the user
        left = self.grid_margin + self.selected_cell['col'] * (self.cell_size + self.cell_margin)
        top =  self.grid_margin + self.selected_cell['row'] * (self.cell_size + self.cell_margin)
        self.textbox_rect = pygame.Rect(left,top,self.cell_size, self.cell_size)
        while True:
            self.calculate_duration()
            self.input_text= self.selected_cell['candidate']
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.unicode.isdigit():
                        self.input_text += event.unicode
                    elif event.key == pygame.K_RETURN:
                        print("Entered text:", self.input_text)
                        self.candidate_mode=False
                        self.selected_cell['candidate']=self.input_text
                        return
                    elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                        self.input_text = self.input_text[:-1]
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.candidate_mode=False
                    return
            self.selected_cell['candidate']=self.input_text                   
            self.draw_window()
    
    def start_new_game(self):
        #start a new game
        self.selected_cell=None
        grid,solution =  generate_sudoku() 
        game = SudokuGame(grid,solution)
        game.run()

    def reinitialize_grid(self):
        # restaore the grid to it's initial state
        for cell in self.cells:
            if cell['editable']:
                cell['value']=0
                cell['candidate']=""
   
    def solve_grid(self):
        # resoudre la grille initiale
        current_grid = [[0 for _ in range(9)] for _ in range(9)]
        for cell in self.cells:
            if not cell['editable']:
                current_grid[cell["row"]][cell["col"]] = cell['value']
        solve(current_grid)
        for cell in self.cells:
            cell['value'] = current_grid[cell['row']][cell['col']]        
     
      
        
        
                   
    def handle_events(self):
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                self.handle_pause_button(pos)
                if self.pause_button['on_pause']:
                    break
                self.handle_menu_click(pos)  # Gérer le clic sur le bouton de menu ou sur une option de menu
                for cell in self.cells:
                    if cell['rect'].collidepoint(pos):
                        self.select_cell(cell)
                        break
            elif event.type == pygame.MOUSEBUTTONUP and not self.pause_button['on_pause']:
                if event.button==3:
                    self.candidate_mode = not self.candidate_mode
                    if self.candidate_mode and self.selected_cell:
                        if self.selected_cell['editable']:
                            self.update_candidate()
                    self.candidate_mode=False
                    self.selected_cell=None
            elif event.type == pygame.KEYDOWN and not self.pause_button['on_pause']:
                if self.selected_cell and self.selected_cell['editable']:
                    if event.unicode.isdigit():
                            self.selected_cell['value'] = int(event.unicode)
                            self.selected_cell = None
                    elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                        self.selected_cell['value'] = 0
                        self.selected_cell = None
            elif event.type == pygame.MOUSEMOTION:
                if self.menu_open:
                    for index, option_rect in enumerate(self.menu_option_rects):
                        if option_rect.collidepoint(event.pos):
                            self.hovered_option = index  # Mettre à jour l'option survolée
                        else:
                            self.hovered_option = None  # Réinitialiser l'option survolée
                
                if self.pause_button['rect'].collidepoint(event.pos):
                    self.pause_button['hovered']=True
                else:
                    self.pause_button['hovered']=False

    def grid_completed(self):
        for cell in self.cells:
            if cell['value'] != self.solution[cell['row']][cell['col']]:
                return False
        return True

    def calculate_duration(self):
        if not self.grid_completed():
            if self.pause_button['on_pause']:
                self.pause_button['duration'] = time.time()- self.pause_button['start_time']
            else:
                elapsed_time = time.time() - self.start_time - self.paused_time
                # Conversion du temps en heure minutes et secondes
                self.duration_heures = int(elapsed_time//3600)
                self.duration_minutes = int(int(elapsed_time % 3600)//60)
                self.duration_secondes=int(int(int(elapsed_time % 3600)%60))
        


    def play_game(self):
        while True:
            self.calculate_duration()
            self.handle_events()
            self.draw_window()
    
           
    def run(self):
        self.play_game()    

if __name__ == '__main__':

    grid,solution =  generate_sudoku() 
    game = SudokuGame(grid,solution)
    game.run()
