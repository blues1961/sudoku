import pygame
import random
from sudoku_generator import *

class SudokuGame:
    def __init__(self,grid,solution):
        if not grid:
           grid = [[0] * 9 for _ in range(9)]
        
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 900))
        pygame.display.set_caption("Sudoku Game")

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.font = pygame.font.Font(None, 46)
        self.font_candidate = pygame.font.Font(None,25)
        self.cell_size = 90
        self.cell_margin = 0
        self.board_margin = 20

        self.board = grid
        self.solution=solution

        self.selected_cell = None
        self.game_started = False
        self.create_widgets()

        self.initial_color=pygame.Color(random.randint(190,220),random.randint(190,220),random.randint(190,220))
        self.completed_color=pygame.Color(random.randint(220,250),random.randint(220,250),random.randint(220,250))

        self.dernier_clic = None
    
        self.textbox_rect = pygame.Rect(0,0,0,0)
        self.input_text = ""                    
        self.textbox_active = False
        self.candidate_mode = False

        self.sauvegarder_grille_sudoku()
    
    
    def sauvegarder_grille_sudoku(self):
        # Convertir la grille en une chaîne de caractères
        chaine_grille = ''.join(str(chiffre) for ligne in self.board for chiffre in ligne)
        # Écrire la chaîne de caractères dans le fichier
        with open('sudoku.txt', 'w') as fichier:
            fichier.write(chaine_grille)
  
    def start_new_game(self):
        self.game_started=True
        self.draw_board()

    def load_saved_game(self):
        self.game_started=True
        

    def create_widgets(self):
        
        self.cells = [{'rect': pygame.Rect(self.board_margin + j * (self.cell_size + self.cell_margin),
                                   self.board_margin + i * (self.cell_size + self.cell_margin),
                                   self.cell_size, self.cell_size),
               'value': self.board[i][j],
               'row': i,
               'col': j,
               'editable': self.board[i][j] == 0,
               'candidate': ""}
              for i in range(9) for j in range(9)]

        
        self.selected_rect = pygame.Rect(0, 0, self.cell_size, self.cell_size)
        self.selected_rect_color = pygame.Color('blue')
    
    def draw_board(self):
        
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
            
            pygame.draw.rect(self.screen, pygame.Color('black'), cell['rect'],1)
     
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
            
            if self.textbox_active:
                    pygame.draw.rect(self.screen, pygame.Color('white'), self.textbox_rect)
                    pygame.draw.rect(self.screen, pygame.Color('red'), self.textbox_rect,4)
                    text = self.font_candidate.render(self.selected_cell['candidate'], True, pygame.Color('black'))
                    text_rect = text.get_rect(center=self.textbox_rect.center)
                    self.screen.blit(text, text_rect)
                    
                           
 
    
        pygame.display.flip()

    def select_cell(self, cell):
        self.selected_cell = cell
        self.selected_rect.topleft = cell['rect'].topleft
    
    def update_candidate(self):
        left = self.board_margin + self.selected_cell['col'] * (self.cell_size + self.cell_margin)
        top =  self.board_margin + self.selected_cell['row'] * (self.cell_size + self.cell_margin)
        self.textbox_rect = pygame.Rect(left,top,self.cell_size, self.cell_size)
        while True:
            self.textbox_active=True
            self.input_text= self.selected_cell['candidate']
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.unicode.isdigit():
                        self.input_text += event.unicode
                    elif event.key == pygame.K_RETURN:
                        print("Entered text:", self.input_text)
                        self.textbox_active=False
                        self.selected_cell['candidate']=self.input_text
                        return
                    elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                        self.input_text = self.input_text[:-1]
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.textbox_active=False
                    return
            self.selected_cell['candidate']=self.input_text                   
            self.draw_board()
                
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            elif event.type==pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for cell in self.cells:
                    if cell['rect'].collidepoint(pos):
                        self.select_cell(cell)
                        break

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button==3:
                    self.candidate_mode = not self.candidate_mode
                    if self.candidate_mode and self.selected_cell:
                        if self.selected_cell['editable']:
                            self.update_candidate()
                    self.candidate_mode=False
                    self.selected_cell=None
            elif event.type == pygame.KEYDOWN:
                if self.selected_cell and self.selected_cell['editable']:
                    if event.unicode.isdigit():
                            self.selected_cell['value'] = int(event.unicode)
                            self.selected_cell = None
                    elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                        self.selected_cell['value'] = 0
                        self.selected_cell = None
  

    def grid_completed(self):
        for cell in self.cells:
            if cell['value'] != self.solution[cell['row']][cell['col']]:
                return False
        return True

    def play_game(self):
        while True:
            self.handle_events()
            self.draw_board()
           
    def run(self):
        self.play_game()    
            

if __name__ == '__main__':
    grid,solution =  generate_sudoku() 
    game = SudokuGame(grid,solution)
    game.run()
