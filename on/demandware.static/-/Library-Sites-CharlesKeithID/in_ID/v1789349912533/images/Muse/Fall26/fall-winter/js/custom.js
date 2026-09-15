
// Burger menu toggle
document.addEventListener('DOMContentLoaded', function() {
    var burgerButton = document.querySelector('.burger-button');
    var menu = document.querySelector('.menu-wrapper');
    var body = document.querySelector('body');
    // var body = document.querySelector('.scroll-wrapper');
    var menCon = document.querySelector('.main-wrapper');

    burgerButton.addEventListener('click', function() {
        console.log('click menu');
        menu.classList.toggle('active');
        burgerButton.classList.toggle('close-bm');
        menCon.classList.toggle('menu-open');
        body.classList.toggle('opened');
    });

    // Remove all menu-related classes when resizing window
    window.addEventListener('resize', function() {
        if (window.innerWidth > 991) {
            menu.classList.remove('active');
            burgerButton.classList.remove('close-bm');
            menCon.classList.remove('menu-open');
            body.classList.remove('opened');
        }
    });


    // add scroll class using sentinel as there is overflow-x hidden set for cursor
    (function () {
        var THRESHOLD_PX = 180;
        var userHasScrolled = false;
        var sentinel = document.createElement('div');

        sentinel.style.position = 'absolute';
        sentinel.style.top = THRESHOLD_PX + 'px';
        sentinel.style.width = '1px';
        sentinel.style.height = '1px';
        sentinel.style.pointerEvents = 'none';
        sentinel.style.opacity = '0';
        document.body.appendChild(sentinel);

        var observer = new IntersectionObserver(function (entries) {
            if (!userHasScrolled) return;

            entries.forEach(function (entry) {
            // Check if sentinel is above the viewport
            if (entry.boundingClientRect.top > 0) {
                // sentinel is still visible - above threshold
                document.body.classList.remove('scroll');
            } else {
                // sentinel above viewport - below threshold
                document.body.classList.add('scroll');
            }
            });
        }, {
            root: null,
            threshold: 0
        });

        observer.observe(sentinel);

        // Only activate tracking after actual scroll
        function activateTracking() {
            userHasScrolled = true;
        }

        window.addEventListener('wheel', activateTracking, { once: true });
        window.addEventListener('touchmove', activateTracking, { once: true });
    })();
});

