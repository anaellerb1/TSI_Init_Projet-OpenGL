#!/usr/bin/env python3

import OpenGL.GL as GL
import glfw
import numpy as np
import tools 
import pyrr
from ctypes import sizeof, c_float, c_void_p
from shapes import get_plane
class Game(object):
    """ Classe principale : fenêtre GLFW avec OpenGL """

    def __init__(self):
        self.window = self.init_window()
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
        sommets, indices = get_plane()
        self.nb_indices = len(indices)

        # Création du VAO : pour les attributs de sommets (positions, normales, couleurs, UV)
        self.vao = GL.glGenVertexArrays(1) # Génération d'un VAO
        GL.glBindVertexArray(self.vao) # On lie le VAO pour l'utiliser

        # Création du VBO : pour les sommets
        self.vbo = GL.glGenBuffers(1) 
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, sommets.nbytes, sommets, GL.GL_STATIC_DRAW) # On envoie les données du VBO dans la mémoire GPU : nbytes = nombre d'octets

        # Création de l'EBO (Element Buffer Object = indices)
        self.ebo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL.GL_STATIC_DRAW)
        
        # Configuration des attributs (position, normale, couleur, UV)
        octets_par_sommet = 6 * sizeof(c_float) 

        octets_par_sommet = 6 * sizeof(c_float)

        position_location = GL.glGetAttribLocation(self.program, "position")
        GL.glVertexAttribPointer(position_location, 3, GL.GL_FLOAT, GL.GL_FALSE, octets_par_sommet, c_void_p(0))
        GL.glEnableVertexAttribArray(position_location)

        couleur_location = GL.glGetAttribLocation(self.program, "couleur")
        GL.glVertexAttribPointer(couleur_location, 3, GL.GL_FLOAT, GL.GL_FALSE, octets_par_sommet, c_void_p(3 * sizeof(c_float)))
        GL.glEnableVertexAttribArray(couleur_location)


        # normale_location = GL.glGetAttribLocation(self.program, "normale")
        # GL.glVertexAttribPointer(normale_location, 3, GL.GL_FLOAT, GL.GL_FALSE, octets_par_sommet, c_void_p(3 * sizeof(c_float)))
        # GL.glEnableVertexAttribArray(normale_location)


        # uv_location = GL.glGetAttribLocation(self.program, "uv")
        # GL.glVertexAttribPointer(uv_location, 2, GL.GL_FLOAT, GL.GL_FALSE, octets_par_sommet, c_void_p(9 * sizeof(c_float)))
        # GL.glEnableVertexAttribArray(uv_location)

       
        pass

    def run(self):
        """
        boucle principale du programme : affichage et gestion des évènements
        :return: None
        """
        # Boucle principale du jeu
        while not glfw.window_should_close(self.window):
            #GL.glClearColor(0.1, 0.1, 0.1, 1.0) # Couleur de fond de la fenêtre ici gris foncé
            GL.glClearColor(1.0, 1.0, 1.0, 1.0)
            
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            # Matrice de vue : caméra positionnée à (0, 0, 3) regardant vers l'origine
            #projection = pyrr.matrix44.create_perspective_projection_matrix(45, 1, 0.1, 100)
            #loc_proj = GL.glGetUniformLocation(self.program, "projection")
            #GL.glUniformMatrix4fv(loc_proj, 1, GL.GL_FALSE, projection)

            # Matrice modèle : translation pour éloigner le plan
            #model = pyrr.matrix44.create_from_translation([0, 0, -3])
            #loc_model = GL.glGetUniformLocation(self.program, "model")
            #GL.glUniformMatrix4fv(loc_model, 1, GL.GL_FALSE, model)


            # Dessin du plan
            GL.glBindVertexArray(self.vao)
            print("Drawing VAO", self.vao, "with", self.nb_indices, "indices")
            GL.glDrawElements(GL.GL_TRIANGLES, self.nb_indices, GL.GL_UNSIGNED_INT, None)



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

def main():
    game = Game()
    game.run()
    glfw.terminate()

if __name__ == '__main__':
    main()
