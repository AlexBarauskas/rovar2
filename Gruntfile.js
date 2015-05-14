module.exports = function(grunt) {
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        concat: {
            dist: {
                src: [
                    'onbike/static/js/jquery.min.js',
                    'onbike/static/js/jquery.form.js',
                    'onbike/static/js/fotorama.js',
                    'onbike/static/js/jquery.smartbanner.min.js',
                    'onbike/static/js/jquery.inputmask.js',
                    'onbike/static/js/jquery.inputmask.extensions.js',
                    'onbike/static/leaflet73/leaflet-src.js',
                    'onbike/static/leaflet73/leaflet.js',
                    'onbike/static/js/moxie/moxie.min.js',
                    'onbike/static/js/customupload.js',
                    'onbike/static/js/intro.js',
                    'map/static/js/map.api.translate.js',
                    'map/static/js/map.api.js',

                    'onbike/static/js/ready.js',
                ],
                dest: 'onbike/static/js/script.js',
            }
        },
        uglify: {
            build: {
                src: 'onbike/static/js/script.js',
                dest: 'onbike/static/js/script.min.js'
            }
        },

        cssmin: {
            options: {
                banner: '/* _ */'
            },
            combine: {
                files: {
                    'onbike/static/css/style.min.css': [
                    'onbike/static/css/reset.css', 
                    'onbike/static/css/clearfix.css', 
                    'onbike/static/leaflet73/leaflet.css',
                    'onbike/static/css/jquery.smartbanner.min.css',
                    'onbike/static/css/introjs.css',
                    'onbike/static/css/fotorama.css',

                    'account/static/account.css',
                    'account/static/account/css/login.css',
                    'onbike/static/css/fonts.css',
                    'onbike/static/css/manager.css',
                    'onbike/static/css/main.css',
                    ],
                }
            }
        },
    });

    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-cssmin');

    grunt.registerTask('default', ['css', 'js']);
    grunt.registerTask('js', ['concat', 'uglify']);
    grunt.registerTask('css', ['cssmin']);

};