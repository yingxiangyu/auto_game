import utils

games = utils.new_set_game_pos()
games[0].init_points()
image = games[0].get_window_img()
image.save("window_screenshot.png")
