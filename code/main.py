#!/usr/bin/env python3

import OpenGL.GL as GL
import glfw
import numpy as np
import tools 
import pyrr
from ctypes import sizeof, c_float, c_void_p
from PIL import Image

class Game(object):
    """ fenêtre GLFW avec openGL """

    def __init__(self):
        self.window = self.init_window()

        self.color = [1.0, 0.0, 0.0]  # rouge par défaut
        self.fov = 50.0 

        self.x = 0.0
        self.y = 0.0
        self.z = -5

        
        self.i = 0
        self.j = 0

        self.k = 0

        #projection
        self.fov = 45

        self.init_context()
        self.init_programs()

        self.texture = self.load_texture("texture/texture1.jpg")

        self.init_data()

    def init_window(self):
        """ 
        création de la fenêtre et initialisation de la librairie glfw et du contexte opengl associé

        :return: la fenêtre créée
        """
        # initialisation de la librairie glfw et du context opengl associé
        glfw.init()
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        # création et parametrage de la fenêtre
        glfw.window_hint(glfw.RESIZABLE, False)
        window = glfw.create_window(800, 800, 'OpenGL', None, None)
        # parametrage de la fonction de gestion des évènements
        glfw.set_key_callback(window, self.key_callback)
        return window

    def init_context(self):
        """
        initialisation du contexte opengl associé à la fenêtre
        :return: None
        """
        # activation du context OpenGL pour la fenêtre
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        # activation de la gestion de la profondeur
        GL.glEnable(GL.GL_DEPTH_TEST)
        #GL.glDisable(GL.GL_DEPTH_TEST)

    def init_programs(self):
        self.program = tools.create_program_from_file("code/phong.vert", "code/phong.frag")
        if self.program:
            GL.glUseProgram(self.program)

        pass
        
    def init_data(self):
        #sommets triangles
        p1 = (0, 0, 0)
        p2 = (1, 0, 0)
        p3 = (0, 1, 0)
        p4 = (0, 0, 1)

        #normales triangles
        n1 = (0.0, 0.0, 1.0)
        n2 = (-0.5774, -0.5774, -0.5774)
        n3 = (-0.5774, -0.5774, -0.5774)
        n4 = (-0.5, -0.5, 0.707)    

        #sommets floor
        p5 = (-5, 0, -5) # point bas gauche
        p6 = (5, 0, -5) # point bas droit
        p7 = (-5, 0, 5) # point haut gauche
        p8 = (5, 0, 5)  # point haut droit


        #normales floor
        n5 = (0.0, 1.0, 0.0)
        n6 = (0.0, 1.0, 0.0)
        n7 = (0.0, 1.0, 0.0)
        n8 = (0.0, 1.0, 0.0)

        # couleurs
        rouge = (1, 0, 0)
        vert = (0, 1, 0)
        bleu = (0, 0, 1)
        jaune = (1, 1, 0)

        #uv (les coordonnées de texture) 
        uv0, uv1, uv2, uv3 = np.array((0, 0), np.float32), np.array((1, 0), np.float32), np.array((0, 1), np.float32), np.array((1, 1), np.float32)

        uv4, uv5, uv6, uv7 = np.array((0, 0), np.float32), np.array((1, 0), np.float32), np.array((0, 1), np.float32), np.array((1, 1), np.float32)

        sommets = np.array([
                *p1, *n1, *rouge, *uv0,
                *p2, *n2, *vert,  *uv1,
                *p3, *n3, *bleu,  *uv2,
                *p4, *n4, *jaune, *uv3], dtype=np.float32)
        
        # sommets floor
        sommets_floor = np.array([
                *p5, *n5, *rouge, *uv4,
                *p6, *n6, *vert,  *uv5,
                *p7, *n7, *bleu,  *uv6,
                *p8, *n8, *jaune, *uv7], dtype=np.float32)


        index = np.array(((0, 1, 2),(1, 3, 2),), dtype=np.uint32)
        index_floor = np.array(((0, 1, 2),(1, 3, 2),), dtype=np.uint32)
        
        # stride : nombre d'octets entre le début de deux sommets consécutifs
        stride = 11 * sizeof(c_float)        

        vao_floor = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vao_floor)

        # VBO de sommets
        vbo_floor = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo_floor)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, sommets_floor, GL.GL_STATIC_DRAW)

        # VBO d'indices (lié AU VAO actif)
        vboi_floor = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, vboi_floor)
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, index_floor, GL.GL_STATIC_DRAW)


        vbo_floor = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo_floor)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, sommets_floor, GL.GL_STATIC_DRAW)
        # Attribut position (location = 0)
        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, stride, c_void_p(0))
        # Attribut normale (location = 1)
        GL.glEnableVertexAttribArray(1)
        GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, GL.GL_FALSE, stride, c_void_p(3 * sizeof(c_float)))
        # Attribut couleur (location = 2)
        GL.glEnableVertexAttribArray(2)
        GL.glVertexAttribPointer(2, 3, GL.GL_FLOAT, GL.GL_FALSE, stride, c_void_p(6 * sizeof(c_float)))
        # Attribut UV (location = 3)
        GL.glEnableVertexAttribArray(3)
        GL.glVertexAttribPointer(3, 2, GL.GL_FLOAT, GL.GL_FALSE, stride, c_void_p(9 * sizeof(c_float)))
       

             



        # 1. Créer le VAO
        vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vao)

        # 2. Créer le VBO (positions)
        vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, sommets, GL.GL_STATIC_DRAW)
    
        # 3. Activer l'attribut position (location = 0)
        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, stride, c_void_p(0))

        # 4. Activer l'attribut normale (location = 1)
        GL.glEnableVertexAttribArray(1)
        GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, GL.GL_FALSE, stride, c_void_p(3 * sizeof(c_float)))

        # 5. Attribut couleur (location = 2)
        GL.glEnableVertexAttribArray(2)
        GL.glVertexAttribPointer(2, 3, GL.GL_FLOAT, GL.GL_FALSE, stride, c_void_p(6 * sizeof(c_float)))

        # 5. Attribut UV (location = 3)
        GL.glEnableVertexAttribArray(3)
        GL.glVertexAttribPointer(3, 2, GL.GL_FLOAT, GL.GL_FALSE, stride, c_void_p(9 * sizeof(c_float)))

        # 6. Créer les VBO d'indices
        vboi = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, vboi)
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, index, GL.GL_STATIC_DRAW)

        self.vao_obj = vao
        self.vao_floor = vao_floor

        self.nb_indices_obj = len(index.flatten())
        self.nb_indices_floor = len(index_floor.flatten())


        pass

    def run(self):
        """
        boucle principale du programme : affichage et gestion des évènements
        :return: None
        """
        # boucle d'affichage
        while not glfw.window_should_close(self.window):
            speed = 0.1

            # changer la couleur de fond en fonction du temps qui passe
            time = glfw.get_time()
            color = np.sin(time)
            GL.glClearColor(color, 0.5, 0.5, 0.5)

            # nettoyage de la fenêtre : fond et profondeur
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
            color_location = GL.glGetUniformLocation(self.program, "uColor")

            # touches directionnelles
            if glfw.get_key(self.window, glfw.KEY_LEFT) == glfw.PRESS:
                self.x -= speed
            if glfw.get_key(self.window, glfw.KEY_RIGHT) == glfw.PRESS:
                self.x += speed
            if glfw.get_key(self.window, glfw.KEY_UP) == glfw.PRESS:
                self.y += speed
            if glfw.get_key(self.window, glfw.KEY_DOWN) == glfw.PRESS:
                self.y -= speed


            # touches de rotation
            if glfw.get_key(self.window, glfw.KEY_I) == glfw.PRESS:
                self.i += speed
            if glfw.get_key(self.window, glfw.KEY_J) == glfw.PRESS:
                self.i -= speed
            if glfw.get_key(self.window, glfw.KEY_K) == glfw.PRESS:
                self.j += speed
            if glfw.get_key(self.window, glfw.KEY_L) == glfw.PRESS:
                self.j -= speed

            
            # touches de profondeur
            if glfw.get_key(self.window, glfw.KEY_Y) == glfw.PRESS:
                self.z += speed
            if glfw.get_key(self.window, glfw.KEY_H) == glfw.PRESS:
                self.z -= speed
            
            xrotation = pyrr.matrix44.create_from_x_rotation(self.i)
            yrotation = pyrr.matrix44.create_from_y_rotation(self.j)
            rotation = xrotation @ yrotation


            GL.glUniform3fv(color_location, 1, self.color)

  
            # Recupère l'identifiant du programme courant
            prog = GL.glGetIntegerv(GL.GL_CURRENT_PROGRAM)
            

            projection = pyrr.matrix44.create_perspective_projection_matrix(self.fov, 1, 0.5, 10)

            loc_proj = GL.glGetUniformLocation(prog, "projection")
            if loc_proj == -1:
                print("Pas de variable uniforme : projection")
            GL.glUniformMatrix4fv(loc_proj, 1, GL.GL_FALSE, projection)


            loc_trans = GL.glGetUniformLocation(prog, "translation")
            if loc_trans == -1 :
                print("Pas de variable uniforme : translation")
                # Modifie la variable pour le programme courant
            GL.glUniform4f(loc_trans, self.x, self.y, self.z, 1.0)


            loc_rot = GL.glGetUniformLocation(prog, "rotation")
            if loc_rot  == -1 :
                print("Pas de variable uniforme : rotation")
            GL.glUniformMatrix4fv(loc_rot, 1, GL.GL_FALSE, rotation)

            GL.glActiveTexture(GL.GL_TEXTURE0)
            GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture)

            # Envoie l’indice 0 dans le sampler du shader
            loc_tex = GL.glGetUniformLocation(self.program, "texture0")
            if loc_tex  == -1 :
                print("Pas de variable uniforme : texture")
            GL.glUniform1i(loc_tex , 0)

            # Objet 1
            GL.glBindVertexArray(self.vao_obj)  # <- bind des triangles
            GL.glUniform4f(loc_trans, self.x, self.y, self.z, 1.0)
            GL.glUniformMatrix4fv(loc_rot, 1, GL.GL_FALSE, rotation)
            GL.glDrawElements(GL.GL_TRIANGLES, self.nb_indices_obj, GL.GL_UNSIGNED_INT, None)


            # Objet 2 
            x2 = self.x + 1.0
            GL.glUniform4f(loc_trans, x2, self.y, self.z, 1.0)
            GL.glUniformMatrix4fv(loc_rot, 1, GL.GL_FALSE, rotation)
            GL.glDrawElements(GL.GL_TRIANGLES, self.nb_indices_obj, GL.GL_UNSIGNED_INT, None)


            # Objet 3: statique (fait office de sol)
            GL.glBindVertexArray(self.vao_floor)
            GL.glUniform4f(loc_trans, 0.0, -2.0, -15.0, 1.0)
            GL.glUniformMatrix4fv(loc_rot, 1, GL.GL_FALSE, pyrr.matrix44.create_identity())
            GL.glDrawElements(GL.GL_TRIANGLES, self.nb_indices_floor, GL.GL_UNSIGNED_INT, None)


            ## dessin des sommets
            #GL.glDrawArrays(GL.GL_LINE_LOOP, 0, 3) #GL_LINE_LOOP : ne rempli pas le triangle
            #GL.glDrawArrays(GL.GL_TRIANGLES, 0, 6)
            #GL.glDrawElements(GL.GL_TRIANGLES, 2*3, GL.GL_UNSIGNED_INT, None)
            glfw.swap_buffers(self.window)
            glfw.poll_events()

    def key_callback(self, win, key, scancode, action, mods):
        # sortie du programme si appui sur la touche 'echap'
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(win, glfw.TRUE)

        if action == glfw.PRESS:
            if key == glfw.KEY_R:
                self.color = [1.0, 0.0, 0.0]
            elif key == glfw.KEY_G:
                self.color = [0.0, 1.0, 0.0]
            elif key == glfw.KEY_B:
                self.color = [0.0, 0.0, 1.0]
            elif key == glfw.KEY_SPACE:
                self.translation = [0.0, 0.0]   
                self.i = 0.0
                self.j = 0.0
                self.fov = 50.0

    def load_texture(self, path):
        image = Image.open(path).transpose(Image.FLIP_TOP_BOTTOM).convert("RGB")
        img_data = np.array(image, dtype=np.uint8)

        texture_id = GL.glGenTextures(1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, texture_id)

        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGB,
                        image.width, image.height, 0,
                        GL.GL_RGB, GL.GL_UNSIGNED_BYTE, img_data)

        GL.glGenerateMipmap(GL.GL_TEXTURE_2D)

        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR_MIPMAP_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)

        return texture_id
     



def main():
    g = Game()
    g.run()
    glfw.terminate()

if __name__ == '__main__':
    main()



"""
### Réponses aux questions
Q_5 : 
    En comptant le nombre de ligne pour une seconde, on a 60 images par seconde.
    Cela correspond à un temps d'affichage de 16.67 ms par image.

Q_25 : 
    L’opération mathematique principale est la division par w (division perspective) suivie d’un changement d’échelle pour passer de [-1, 1] à [0, width/height].

Q_56 : 
    Les coordonnées de texture (UV) en OpenGL sont normalisées entre 0.0 et 1.0.
    Mais si on sort de cette plage, OpenGL applique un "wrap" (enroulement).
    Cela signifie que si les coordonnées UV sont en dehors de [0, 1], elles seront répétées.

Q_57 :
    Mode	            Effet
    GL_REPEAT	        Répète la texture (défaut)
    GL_CLAMP_TO_EDGE	Reste figé à la dernière valeur valide
    GL_MIRRORED_REPEAT	Répète mais miroir à chaque cycle
    GL_CLAMP_TO_BORDER	Colore avec une couleur définie
"""