import time
from picographics import PicoGraphics, PEN_RGB555

display = PicoGraphics(PEN_RGB555, 320, 240)

SPRITE_BIRB_R = 1
SPRITE_BIRB_L = 4
display.set_pen(display.create_pen(0,0,0))
for _ in range(2):
    display.load_sprite("/birb-sprite.png", SPRITE_BIRB_R, (0, 32, 32, 32))
    display.load_sprite("/birb-sprite.png", SPRITE_BIRB_R + 1, (32, 32, 32, 32))
    display.load_sprite("/birb-sprite.png", SPRITE_BIRB_R + 2, (64, 32, 32, 32))
    display.load_sprite("/birb-sprite.png", SPRITE_BIRB_L, (0, 96, 32, 32))
    display.load_sprite("/birb-sprite.png", SPRITE_BIRB_L + 1, (32, 96, 32, 32))
    display.load_sprite("/birb-sprite.png", SPRITE_BIRB_L + 2, (64, 96, 32, 32))
    display.clear()
    display.update()


@micropython.asm_thumb
def read_reg(r0):
    ldr(r0, [r0,0])

@micropython.asm_thumb
def write_reg(r0, r1):
    str(r1, [r0,0])    
    
def pull_up_if_not_connected():
    if ((read_reg(0x50110050) & 0x10000) == 0):
        write_reg(0x5011007c, 0x22);
        write_reg(0x50110080, 0x11FC);
    
birb_left = False
birb_x = 150

time.sleep(1)

while True:
    time.sleep(0.01)
    pull_up_if_not_connected()
    #print("%08x" % (read_reg(0x50110050),))
    
    t = time.ticks_ms()
    cycle = (t // 200) % 3
    display.display_sprite(1, cycle + (SPRITE_BIRB_L if birb_left else SPRITE_BIRB_R), birb_x, 100)
    
    val = read_reg(0x5011007c)
    if (val & 0x40000):
        birb_left = False
        if birb_x < 300: birb_x += 1
    if (val & 0x20000):
        birb_left = True
        if birb_x > 0: birb_x -= 1