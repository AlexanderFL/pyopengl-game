
attribute vec3 a_position;
attribute vec3 a_normal;
attribute vec2 a_uv;

uniform mat4 u_model_matrix;
uniform mat4 u_view_matrix;
uniform mat4 u_projection_matrix;

uniform vec4 u_eye_position;
uniform vec4 u_light_position;

// varying vec4 v_color;

varying vec4 v_normal;
varying vec4 v_s;
varying vec4 v_h;
varying vec2 v_uv;

void main(void)
{
    vec4 position   = vec4(a_position.x, a_position.y, a_position.z, 1.0);
    vec4 normal     = vec4(a_normal.x, a_normal.y, a_normal.z, 0.0);

    // UV coords sent into per-pixel use
    v_uv = a_uv;

    position        = u_model_matrix * position;
    v_normal          = u_model_matrix * normal;

    v_s             = u_light_position - position;
    // float lambert   = max(0.0, dot(normal, s) / (length(normal) * length(s)));
    // v_color      = u_light_diffuse * u_material_diffuse * lambert;

    vec4 v          = u_eye_position - position;
    v_h             = v_s + v;
    // float phong     = max(0.0, dot(normal, h) / (length(normal) * length(h)));

    // v_color         = u_light_diffuse * u_material_diffuse * lambert
    //                + u_light_specular * u_material_specular * pow(phong, u_material_shininess);

    position        = u_view_matrix * position;
    position        = u_projection_matrix * position;

    gl_Position     = position;
}