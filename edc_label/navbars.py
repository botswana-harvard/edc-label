from edc_navbar import Navbar, NavbarItem, site_navbars


label = Navbar(name='edc_label')

label.append_item(
    NavbarItem(name='label',
               label='Label',
               fa_icon='fa-film',
               url_name='edc_label:home_url'))

site_navbars.register(label)
