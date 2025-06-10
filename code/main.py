#!/usr/bin/env python3

import OpenGL.GL as GL
import glfw
import numpy as np
import tools 
import pyrr


from PIL import Image
from ctypes import sizeof, c_float, c_void_p
from shapes import get_plane, get_cube
class Game(object):
    """ Classe principale : fenêtre GLFW avec OpenGL """

    def __init__(self):
        self.window = self.init_window()

        self.fov = 50.0 
        self.x = 0.0
        self.y = 0.0
        self.z = -5
        self.i = 0
        self.j = 0
        self.k = 0

        self.init_context()
        self.init_programs()
        self.init_data()

    def init_window(self):
        """ 
        création de la fenêtre et initialisation de la librairie glfw et du contexte opengl associé

        :return: la fenêtre créée
        """
        ### note: mettre à chaque fois qu'on utilise GLFW
        glfw.init() 
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.RESIZABLE, False)  #Empêche l'utilisateur de redimensionner la fenêtre

        # Création de la fenêtre GLFW et touches de contrôle
        window = glfw.create_window(1000, 1000, 'Projet OpenGL Anaëlle', None, None)
        glfw.set_key_callback(window, self.key_callback) 
        return window

    def init_context(self):
        """
        initialisation du contexte opengl associé à la fenêtre
        :return: None
        """
        glfw.make_context_current(self.window)
        glfw.swap_interval(1) # attente de la fin du rafraîchissement de l'écran avant de dessiner le prochain frame 1 = active, 0 = désactivé
        GL.glEnable(GL.GL_DEPTH_TEST) 

    def init_programs(self):
        """
        initialisation des programmes OpenGL (shaders) utilisés dans le jeu
        :return: None
        """
        self.program = tools.create_program_from_file("code/shaders/phong.vert", "code/shaders/phong.frag")
        GL.glUseProgram(self.program)
        if self.program <= 0:
            raise Exception("[Erreur] lors de la création du programme OpenGL : fonction init_programs()")

    def init_data(self):
        """
        initialisation des données OpenGL (VBO, VAO, textures, etc.)
        :return: None
        """
        sommets, indices = get_cube() 
        self.nb_indices = len(indices)

        self.vao, self.nb_indices = tools.config_shape(sommets, indices, self.program)

        # Bloc minecraft
        face_terre = self.load_texture("code/assets/faceterre.png")
        face_herbe = self.load_texture("code/assets/faceherbe.png")
        face_cote = self.load_texture("code/assets/facecote.png")
        self.textures = [
            face_cote,  # Face avant
            face_cote,  # Face arrière
            face_cote,  # Droite
            face_cote,  # Gauche
            face_herbe, # Haut
            face_terre,  # Bas
        ]

        # Gestion des textures
        # self.textures = [
        #     self.load_texture("code/assets/1.png"),  # Face avant
        #     self.load_texture("code/assets/2.png"),  # Face arrière
        #     self.load_texture("code/assets/3.png"),  # Droite
        #     self.load_texture("code/assets/4.png"),  # Gauche
        #     self.load_texture("code/assets/5.png"),  # Haut
        #     self.load_texture("code/assets/6.png"),  # Bas
        # ]


        GL.glUseProgram(self.program)
        GL.glUniform1i(GL.glGetUniformLocation(self.program, "tex"), 0)

        pass

    def run(self):
        """
        boucle principale du programme : affichage et gestion des évènements
        :return: None
        """
        # Boucle principale du jeu
        while not glfw.window_should_close(self.window):
            GL.glClearColor(0.1, 0.1, 0.1, 1.0) # Couleur de fond de la fenêtre ici gris foncé
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            # touches directionnelles
            if glfw.get_key(self.window, glfw.KEY_LEFT) == glfw.PRESS:
                self.x -= 0.1
            if glfw.get_key(self.window, glfw.KEY_RIGHT) == glfw.PRESS:
                self.x += 0.1
            if glfw.get_key(self.window, glfw.KEY_UP) == glfw.PRESS:
                self.y += 0.1
            if glfw.get_key(self.window, glfw.KEY_DOWN) == glfw.PRESS:
                self.y -= 0.1

            # touches de profondeur
            if glfw.get_key(self.window, glfw.KEY_Y) == glfw.PRESS:
                self.z += 0.1
            if glfw.get_key(self.window, glfw.KEY_H) == glfw.PRESS:
                self.z -= 0.1

            # touches de rotation
            if glfw.get_key(self.window, glfw.KEY_I) == glfw.PRESS:
                self.i += 0.1
            if glfw.get_key(self.window, glfw.KEY_J) == glfw.PRESS:
                self.i -= 0.1
            if glfw.get_key(self.window, glfw.KEY_K) == glfw.PRESS:
                self.j += 0.1
            if glfw.get_key(self.window, glfw.KEY_L) == glfw.PRESS:
                self.j -= 0.1

            xrotation = pyrr.matrix44.create_from_x_rotation(self.i)
            yrotation = pyrr.matrix44.create_from_y_rotation(self.j)
            rotation = xrotation @ yrotation

            # Gestion de la caméra
            prog = GL.glGetIntegerv(GL.GL_CURRENT_PROGRAM)
            projection = pyrr.matrix44.create_perspective_projection_matrix(self.fov, 1, 0.5, 10)
            
            loc_proj = GL.glGetUniformLocation(prog, "projection")
            GL.glUniformMatrix4fv(loc_proj, 1, GL.GL_FALSE, projection)

            loc_trans = GL.glGetUniformLocation(prog, "translation")
            GL.glUniform4f(loc_trans, self.x, self.y, self.z, 1.0)

            loc_rot = GL.glGetUniformLocation(prog, "rotation")
            GL.glUniformMatrix4fv(loc_rot, 1, GL.GL_FALSE, rotation)

            # Dessin du plan
            GL.glBindVertexArray(self.vao)
            #print("Drawing VAO", self.vao, "with", self.nb_indices, "indices")


            for i in range(len(self.textures)):  
                GL.glBindTexture(GL.GL_TEXTURE_2D, self.textures[i])
                offset = c_void_p(i * len(self.textures) * sizeof(GL.GLuint))
                GL.glDrawElements(GL.GL_TRIANGLES, 6, GL.GL_UNSIGNED_INT, offset)




            glfw.swap_buffers(self.window) # Affichage du contenu de la fenêtre
            glfw.poll_events() # Gestion des évènements (clavier, souris, etc.)

    def key_callback(self, win, key, scancode, action, mods):
        """
        Callback pour la gestion des touches du clavier

        parameters:
            win: la fenêtre GLFW
            key: la touche pressée
            scancode: le code de la touche pressée
            action: l'action effectuée (appui, relâchement, etc.)
            mods: les touches de modification (Shift, Ctrl, etc.)

        return: 
            None
        """
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(win, glfw.TRUE)
    
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
    game = Game()
    game.run()
    glfw.terminate()

if __name__ == '__main__':
    main()
