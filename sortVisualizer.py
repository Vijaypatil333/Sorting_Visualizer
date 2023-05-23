import pygame
import random
import math
pygame.init()

class DrawInformation:
    BLACK = 0,0,0
    WHITE = 255,255,255
    BLUE = 0,0,255
    GREEN = 0,255, 0
    RED = 255,0,0
    BACKGROUND_COLOR = WHITE

    GRADIENTS = [
        (128, 128, 128),
        (160,160,160),
        (192,192,192)
    ]
    FONT = pygame.font.SysFont('comicsans', 20)
    LARGE_FONT = pygame.font.SysFont('comicsans', 40)

    SIDE_PAD = 100 #padding from both side 50 on left 50 on right
    TOP_PAD = 150 #padding from top

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))# to create the pygame window by giving width and height
        pygame.display.set_caption("Sorting Algorithm Visualizer") #name of the window
        self.set_list(lst) 

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)    
        #calculating width of the blocks i.e drawable area
        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        #calculating height of the blocks
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        #calculating x co-ordinate of the blocks
        self.start_x = self.SIDE_PAD //2

#drawing the general screen     
def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR) # fill the background screen
    #To draw controls on the window....1 for sharpens of font and color of the font
    
    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.BLUE)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2, 5))#blit will take surface and blit in window
    
    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2, 55))#blit will take surface and blit in window
    
    sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort | S - Selection Sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2, 85))#35 means 30 pixels below the controls

    draw_list(draw_info)
    pygame.display.update()

#drawing the list
def draw_list(draw_info, color_positions = {}, clear_bg = False):    
    lst = draw_info.lst

    if(clear_bg):#it will create the rectangle of blocks only and clear that rect without affecting controls 
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)


    for i, val in enumerate(lst):#enumerate gives index as well as values
        x = draw_info.start_x + i * draw_info.block_width # to draw block at specific position
        y = draw_info.height - (val- draw_info.min_val) * draw_info.block_height
        

        color = draw_info.GRADIENTS[i % 3]#every three elements will have diff color

        if(i in color_positions):# setting color from dict to the currect processing blocks
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

    if(clear_bg):#clear equals true then update the screen
        pygame.display.update()

def generate_starting_list(n, min_val, max_val):#Generating automatic list(random)
    lst = []
     
    for i in range(n):
       val = random.randint(min_val, max_val)
       lst.append(val)

    return lst   

def bubble_sort(draw_info, ascending = True):
    lst = draw_info.lst

    for i in range(len(lst)-1):
        for j in range(len(lst)-1-i):
            if(lst[j] > lst[j+1] and ascending) or (lst[j] < lst[j+1] and not ascending):
                lst[j], lst[j+1] = lst[j+1], lst[j]
                draw_list(draw_info, {j: draw_info.GREEN, j+1: draw_info.RED}, True)
                #this will help to use the controls like reset ascending etc
                yield True #generator - pause and store the current function and resume it whenever it called again
    return lst            


def insertion_sort(draw_info, ascending = True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending

            if(not ascending_sort and not descending_sort):
                break

            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i: draw_info.GREEN, i-1: draw_info.RED}, True)
            yield True

    return lst    

def selection_sort(draw_info, ascending = True):    
    lst = draw_info.lst

    for i in range(len(lst)):
        if(not ascending):
            min_index = i
            for j in range(i+1, len(lst)):
                if lst[j] > lst[min_index]:
                    min_index = j
        else:
            min_index = i
            for j in range(i+1, len(lst)):
                if lst[j] < lst[min_index]:
                    min_index = j   
        lst[i], lst[min_index] = lst[min_index], lst[i]
        draw_list(draw_info, {i: draw_info.GREEN, min_index: draw_info.RED}, True)  
        yield True  
 
    return lst

def main():
    run = True
    clock = pygame.time.Clock()
    
    n = 50 
    min_val = 0
    max_val = 100

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(800, 600, lst)
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort #name of generator func whch gives generator object
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None #used to store the generator object which has next() func will give next yield function or value

    while run:#to implement pygame make while loop continuously running in background OR it will just print on screen and exit the window
       clock.tick(60)

       if(sorting):#when sorting is true 
           try:#calling the generator untill it is finished 
               next(sorting_algorithm_generator)
           except StopIteration:#give stopIteration which will make sorting equal to false
               sorting = False
       else:
           draw(draw_info, sorting_algo_name, ascending)            

       #pygame.display.update()#to update the display

       for event in pygame.event.get():#returns all of the events that have occurred since the last loop(since last time this was called)
           if(event.type == pygame.QUIT):# to quit the game by clicking x on topmost right corner 
               run = False

           if(event.type != pygame.KEYDOWN):
               continue

           if(event.key == pygame.K_r):#to reset the list by clicking key R
               lst = generate_starting_list(n, min_val, max_val)
               draw_info.set_list(lst)#draw info storing the list so need to reset it into draw info
               sorting = False
           elif(event.key == pygame.K_SPACE and sorting == False):#to start the sorting by clicking key SPACE
               sorting = True
               sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
           elif(event.key == pygame.K_a and not sorting):#to sort in ascending by clicking key A
               ascending = True
           elif(event.key == pygame.K_d and not sorting):#to sort in descending by clicking key D
               ascending = False 
           elif(event.key == pygame.K_i and not sorting):#to apply Insertion sort by clicking key I
               sorting_algorithm = insertion_sort
               sorting_algo_name = "Insertion Sort" 
           elif(event.key == pygame.K_b and not sorting):#to apply Bubble sort by clicking key B
               sorting_algorithm = bubble_sort
               sorting_algo_name = "Bubble Sort"  
           elif(event.key == pygame.K_s and not sorting):#to apply Selection sort by clicking key S
               sorting_algorithm = selection_sort
               sorting_algo_name = "Selection Sort"            

               
                 

    pygame.quit()# ends the pygame program after execution of the loop           

if __name__ == "__main__": # ensures that we actually are running this module by clicking the run button
    main()#or running this module before we call the main function
       