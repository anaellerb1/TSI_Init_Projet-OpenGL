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
        glfw.init()
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.RESIZABLE, False)

        window = glfw.create_window(800, 800, 'Projet OpenGL Anaëlle', None, None)
        glfw.set_key_callback(window, self.key_callback)
        return window

    def init_context(self):
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        GL.glEnable(GL.GL_DEPTH_TEST)

    def init_programs(self):
        self.program = tools.create_program_from_file("shaders/phong.vert", "shaders/phong.frag")
        GL.glUseProgram(self.program)

    def init_data(self):
        # À compléter dans Q1 avec les VBO/VAO pour le plan
        pass

    def run(self):
        while not glfw.window_should_close(self.window):
            GL.glClearColor(0.1, 0.1, 0.1, 1.0)
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            # TODO : dessiner ici avec glBindVertexArray + glDrawElements

            glfw.swap_buffers(self.window)
            glfw.poll_events()

    def key_callback(self, win, key, scancode, action, mods):
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(win, glfw.TRUE)

def main():
    game = Game()
    game.run()
    glfw.terminate()

if __name__ == '__main__':
    main()
