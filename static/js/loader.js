function loadStaticFiles(files) {
    const baseStaticUrl = "/static/";  // Adjust if needed

    files.forEach(file => {
        let fileType = file.split('.').pop();  // Get the file extension

        if (fileType === "css") {
            // Load CSS dynamically
            let link = document.createElement("link");
            link.rel = "stylesheet";
            link.href = baseStaticUrl + file;
            document.head.appendChild(link);
        } 
        else if (fileType === "js") {
            // Load JavaScript dynamically
            let script = document.createElement("script");
            script.src = baseStaticUrl + file;
            script.defer = true;
            document.body.appendChild(script);
        } 
        else {
            console.warn("Unsupported file type:", file);
        }
    });
}

// Example Usage:
loadStaticFiles([
    'js/jquery.js',
    'js/jquery-migrate.min.js',
    'js/plugins/revslider/public/assets/js/jquery.themepunch.tools.min.js',
    'js/plugins/revslider/public/assets/js/jquery.themepunch.revolution.min.js',
    'js/plugins/revslider/public/assets/js/extensions/revolution.extension.slideanims.min.js',
    'js/plugins/revslider/public/assets/js/extensions/revolution.extension.layeranimation.min.js',
    'js/plugins/revslider/public/assets/js/extensions/revolution.extension.kenburn.min.js',
    'js/plugins/revslider/public/assets/js/extensions/revolution.extension.navigation.min.js',
    'js/plugins/revslider/public/assets/js/extensions/revolution.extension.parallax.min.js',  
    'js/plugins/revslider/public/assets/js/extensions/revolution.extension.actions.min.js', 
    'js/plugins/revslider/public/assets/js/extensions/revolution.extension.video.min.js',
    'js/plugins/ui/core.min.js',
    'js/plugins/jquery.requestAnimationFrame.js',
    'js/plugins/ilightbox.packed.js',
    'js/plugins/jquery.easing.js',
    'js/plugins/waypoints.min.js',
    'js/plugins/jquery.isotope.js',
    'js/plugins/jquery.masory.js',
    'js/plugins/jquery.tooltipster.min.js',
    'js/plugins/jarallax.js',
    'js/plugins/jquery.sticky-kit.min.js',
    'js/plugins/jquery.stellar.min.js',
    'js/plugins/jquery.cookie.js',
    'js/plugins/custom_plugins.js',
    'js/plugins/custom.js',
    'js/plugins/custom_onepage.js',
    'js/plugins/jquery.countdown.js',
    'js/plugins/imagesloaded.min.js',
    'js/plugins/masonry.min.js',
    'js/plugins/jquery.simplegmaps.min.js',
    'js/plugins/jarallax-video.js',
    'js/plugins/jquery.cookie.js',
    'js/plugins/custom_clock.js',
    'js/plugins/mediaelement/mediaelementplayer-legacy.min.css',
    'js/plugins/flexslider/flexslider.css',
    'js/plugins/revslider/public/assets/css/settings.css',
    'css/style.css',
    'css/reset.css',
    'css/wordpress.css',
    'css/animation.css',
    'css/ilightbox/ilightbox.css',
    'css/jqueryui/custom.css',
    'css/tooltipster.css',
    'css/odometer-theme-minimal.css',
    'css/odometer-theme-minimal.css',
    'css/menus/leftalignmenu.css',
    'css/font-awesome.min.css',
    'css/themify-icons.css',
    'css/grandconference_custom_css.css',
    'css/kirki-styles.css',
    'css/grid.css',

]);

fetch('/')  // Django view endpoint
    .then(response => response.json())
    .then(data => {
        loadStaticFiles(data.files);  // Call function to load them
    })
    

