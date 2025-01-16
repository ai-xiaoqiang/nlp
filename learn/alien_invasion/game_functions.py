import sys
import pygame
from bullet import Bullet
from alien import Alien

def check_keydown_events(event,ai_settings,screen,ship,bullets):
    if event.key == pygame.K_RIGHT:
            ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets)

def fire_bullet(ai_settings,screen,ship,bullets):
    # 创建一颗子弹，并将其加入到编组bullets中
    if len(bullets) <= ai_settings.bullet_allowed:
        new_bullets = Bullet(ai_settings,screen,ship)
        bullets.add(new_bullets)

def check_keyup_events(event,ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings,screen,ship,bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)

def update_screen(ai_settings,screen,ship,aliens,bullets):
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    # 在飞船和外星人后面重绘子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    # 让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullets(bullets):
    """更新子弹位置并删除已消失的子弹"""
    bullets.update()
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

def create_fleet(ai_settings, screen,ship, aliens):
    """创建外星人群"""
    # 创建一个外星人，并计算一行可容纳多少个外星人
    # 外星人间距为外星人宽度
    alien = Alien(ai_settings,screen)
    number_alien_x = get_number_alien_x(ai_settings,alien.rect.width)
    number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_alien_x):
            create_alien(ai_settings,screen,alien_number,row_number,aliens)
            aliens.add(alien)

def get_number_alien_x(ai_settings,alien_width):
    """计算每行可以容纳的外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_alien_x = int(available_space_x / (2 * alien_width))
    return number_alien_x

def create_alien(ai_settings,screen,alien_number,row_number,aliens):
    alien = Alien(ai_settings,screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def get_number_rows(ai_settings,ship_height,alien_height):
    available_space_y = ai_settings.screen_height - (3 * alien_height ) - ship_height
    numbers_rows = int(available_space_y / (2 * alien_height))
    return numbers_rows


def update_aliens(ai_settings,aliens):
    """更新外星人群组中所有外星人的位置"""
    check_fleet_edges(ai_settings,aliens)
    aliens.update()


def check_fleet_edges(ai_settings,aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break

def change_fleet_direction(ai_settings,aliens):
    """将整群外星人下移，并改变他们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
        ai_settings.fleet_direction *= -1 #这个不懂
        
