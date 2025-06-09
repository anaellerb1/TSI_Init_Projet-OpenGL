#version 330 core

in vec3 v_color;
in vec3 v_normale;
in vec3 frag_pos;
in vec2 frag_uv;

// Déplacements
in vec3 coordonnee_3d;
in vec3 coordonnee_3d_locale;

out vec4 color;

void main() {
    vec3 light_dir = normalize(vec3(0.5, 0.5, 1.0));
    vec3 norm = normalize(v_normale);

    float diffuse = max(dot(norm, light_dir), 0.0);

    vec3 final_color = (0.2 + 0.7 * diffuse) * v_color;
    color = vec4(frag_uv, 0.0, 1.0);

}
