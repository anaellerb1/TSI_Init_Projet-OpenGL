#!/usr/bin/env python3

import OpenGL.GL as GL
import glfw
import numpy as np
import tools 
import pyrr
from ctypes import sizeof, c_float, c_void_p

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

    def init_data(self):
        """
        initialisation des données OpenGL (VBO, VAO, textures, etc.)
        :return: None
        """
        # TODO : compléter dans Q1 avec les VBO/VAO pour le plan
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

            # TODO : dessiner ici avec glBindVertexArray + glDrawElements


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
