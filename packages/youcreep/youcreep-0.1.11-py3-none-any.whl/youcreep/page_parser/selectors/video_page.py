play_btn_sel = '#dismiss-button > yt-button-renderer > yt-button-shape > button'
"""video play button"""

play_on_playing_btn_sel = f'{play_btn_sel}[data-title-no-tooltip="播放"]'
"""video play button when video is playing"""

play_on_pausing_btn_sel = f'{play_btn_sel}[data-title-no-tooltip="暂停"]'
"""video play button when video is pausing"""
