function ThemeCore(){
    this.themeUpdated = () => {
        let reset = false;
        let theme = 'Dark';
        if(Settings){
            reset = Settings.get('thm.reset');
            theme = Settings.get('thm.theme');
        }
		if(theme === 'Custom')	this.setTheme(Settings.get('thm.primaryCol'), Settings.get('thm.readerBg'), Settings.get('thm.accentCol'), Settings.get('thm.textCol'));
		else if (theme === 'Dark')	this.setTheme('#3a3f44', '#272b30', '#b2dffb','#eeeeee');
		else if (theme === 'Reaper') this.setTheme('#272836', '#121223', '#487DE4', '#EEEEEE');
		else if (theme === 'Zaibatsu') this.setTheme('#1D1D1D', '#000000', '#BA1F1F', '#EEEEEE');
		else if (theme === 'Light') this.setTheme('#F1F4FF', '#FFFFFF', '#5889F0','#2B2B2B');
		if(reset === true) this.resetCustom();
	}
	this.setTheme = (sidebar, reader, accent, text) => {
		document.documentElement.style.setProperty("--readerBg", reader);
		document.documentElement.style.setProperty("--sidebarCol", sidebar);
		document.documentElement.style.setProperty("--accentCol", accent);
		document.documentElement.style.setProperty("--textCol", text);
		document.documentElement.style.setProperty("--icoCol", text);
		document.documentElement.style.setProperty("--sidebarColDark", colManipulate(sidebar, -15));
		document.documentElement.style.setProperty("--sidebarColDarkA", colManipulate(sidebar, -15) + '00');
		document.documentElement.style.setProperty("--prevCol", colManipulate(sidebar, -7));

		let [r, g, b] = hexToRgb(accent);
		var	luma = ((r*299)+(g*587)+(b*114))/1000;

		document.documentElement.style.setProperty("--accentSelected", (luma > 160?'#111111':'#ffffff'));
		
		[r, g, b] = hexToRgb(sidebar);
		luma = ((r*299)+(g*587)+(b*114))/1000;

		document.documentElement.style.setProperty("--accentSelectedInvert", (luma < 160?'#444444':'#cccccc')); // Play with 160 there if you want.
		if(luma > 100) { //Tweaks if theme is light
			document.documentElement.style.setProperty("--borderColor", "rgba(0,0,0,0.2)");
			document.documentElement.style.setProperty("--blackLight", "rgba(0,0,0,0.05)");
			document.documentElement.style.setProperty("--sidebarColFocus", colManipulate(sidebar, -24));
		} else {
			document.documentElement.style.setProperty("--borderColor", "rgba(0,0,0,0.7)");
			document.documentElement.style.setProperty("--blackLight", "rgba(0,0,0,0.2)");
			document.documentElement.style.setProperty("--sidebarColFocus", colManipulate(sidebar, -27));
		}
		[r, g, b] = hexToRgb(sidebar)
		let [rt, gt, bt] = hexToRgb(text)
		if(Math.abs(r-rt) < 50
		&& Math.abs(g-gt) < 50
		&& Math.abs(b-bt) < 50) {
			if(luma > 200) {
				document.documentElement.style.setProperty("--rescueShade", '0px 1px 1px rgba(0,0,0,0.6),0px -1px 1px rgba(0,0,0,0.6),-1px 0px 1px rgba(0,0,0,0.6),1px 0px 1px rgba(0,0,0,0.6)');
			}else{
				document.documentElement.style.setProperty("--rescueShade", '0px 1px 1px rgba(255,255,255,0.6),0px -1px 1px rgba(255,255,255,0.6),-1px 0px 1px rgba(255,255,255,0.6),1px 0px 1px rgba(255,255,255,0.6)');
			}
			Tooltippy.set('Contrast ratio too low, safety outline enabled.')
		}else{
			document.documentElement.style.setProperty("--rescueShade", 'unset');
			Tooltippy.reset();
		}

		[r, g, b] = hexToRgb(reader);
		luma = ((r*299)+(g*587)+(b*114))/1000;
		
		if(luma > 100) {
			document.documentElement.style.setProperty("--rdrBorderL", "3px");
			document.documentElement.style.setProperty("--rdr-wb", "1px");
			document.documentElement.style.setProperty("--blackFlag", "rgba(0,0,0,0.3)");
			document.documentElement.style.setProperty("--rdrAncBottomWhite", "rgba(255,255,255,0.6)");
		} else {
			document.documentElement.style.setProperty("--rdrBorderL", "1px");
			document.documentElement.style.setProperty("--rdr-wb", "2px");
			document.documentElement.style.setProperty("--blackFlag", "rgba(0,0,0,0.7)");
			document.documentElement.style.setProperty("--rdrAncBottomWhite", "rgba(255,255,255,0.35)");
		}
	}

	this.resetCustom = () => {
		Settings.set('thm.reset', false);
		if(Settings.get('thm.theme') === 'Custom') {
			Settings.set('thm.primaryCol', '#3A3F44');
			Settings.set('thm.readerBg', '#272B30');
			Settings.set('thm.accentCol', '#B2DFFB');
			Settings.set('thm.textCol', '#EEEEEE');
		}
	}
}

function Serialization(){
	this.all = {};

	this.deserialize = () => {
		if(!localStorage) return;
		var settings = localStorage.getItem('settings');
		try{
			if(!settings) throw 'No settings';
			settings = JSON.parse(settings);
			if(settings.VER && settings.VER != this.ver) {
				throw 'Settings ver changed';
			}
			for(var setting in settings) {
				if(setting == 'VER') continue;
				if(this.set) this.set(setting, settings[setting], true);
				else this.all[setting] = settings[setting];	// should confuse people =))
			}
			return settings;
		}catch (e){
			localStorage.setItem('settings','');
			console.warn('Settings were found to be corrupted and so were reset.');
			for (var setting in this.all) {
				this.all[setting].set(this.all[setting].get());
			}
		}
	}

	this.serialize = function() {
		var settings = {};

		// for site reader screen, settings are packet
		for(var setting in this.all) {
			if(this.all[setting].set) settings[setting] = this.all[setting].get();
			else settings[setting] = this.all[setting];
		}
		// delete groupPreference from localstorage so it does not load preferred group even on better quality release
		delete settings['misc.groupPreference'];
		settings.VER = this.ver;
		return JSON.stringify(settings);
	}
}