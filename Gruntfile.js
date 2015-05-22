var src_js = [  'onbike/static/js/jquery.min.js',
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
                'onbike/static/js/ready.js',]

var src_css =  ['onbike/static/css/reset.css', 
                'onbike/static/css/clearfix.css', 
                'onbike/static/leaflet73/leaflet.css',
                'onbike/static/css/jquery.smartbanner.min.css',
                'onbike/static/css/introjs.css',
                'onbike/static/css/fotorama.css',
                'account/static/account.css',
                'account/static/account/css/login.css',
                'onbike/static/css/fonts.css',
                'onbike/static/css/manager.css',
                'onbike/static/css/main.css',]

module.exports = function(grunt) {
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        concat: {
            dist: {
                src: src_js,
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
                    'onbike/static/css/style.min.css': src_css,
                }
            }
        },

        watch: {
            scripts: {
                files: src_js,
                tasks: ['js'],
                options: {
                    spawn: false,
                },
            },
            html: {
                files: ['*.html'],
                tasks: [],
                options: {
                    spawn: false,
                },
            },
            css: {
                files: src_css,
                tasks: ['css'],
                options: {
                    spawn: false,
                }
            },
        },
    });

    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-contrib-watch');

    grunt.registerTask('default', ['css', 'js', 'watch']);
    grunt.registerTask('js', ['concat', 'uglify']);
    grunt.registerTask('css', ['cssmin']);

};