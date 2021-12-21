
attribute vec2 u_crosshair_position;

varying vec4 u_projection_matrix;

void main()
{
    vec4 position   = vec4(u_crosshair_position.x, u_crosshair_position.y, 0.0, 0.0);

    position        = u_projection_matrix * position;
    gl_Position     = position;
}