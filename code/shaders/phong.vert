#version 330 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec3 normale;
layout (location = 2) in vec3 couleur;
layout (location = 3) in vec2 uv;

out vec3 v_color;
out vec3 v_normale;
out vec3 frag_pos;
out vec2 frag_uv;

void main() {
  gl_Position = vec4(position, 1.0);
  v_color = couleur;

  v_normale = normale;
  frag_pos = position;
  frag_uv = uv;

}
