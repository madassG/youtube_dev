    var previous_elements_count = 10;
    var infinite = new Waypoint.Infinite({
        element: $('.infinite-container')[0],
        handler: function(direction) {
        },
        offset: 'bottom-in-view',

        onBeforePageLoad: function () {
            $('.loading-indicator').show();
        },

        onAfterPageLoad: function () {
            $('.loading-indicator').hide();
            const videoBlocks = document.querySelectorAll('.channel-video-block');
            for (let i = previous_elements_count; i < videoBlocks.length; i++) {
                videoBlocks[i].querySelector('.channel-video-block__short').addEventListener('click', (e) => {
                    let arrow = videoBlocks[i].querySelector('.channel-video-block__arrow').querySelector('img');
                    let bl = videoBlocks[i].querySelector('.channel-video-block-detailed');

                    arrow.style.transform = bl.style.display == 'none' ? 'rotateX(180deg)' : 'none';

                    bl.style.display = bl.style.display == 'none' ? 'grid' : 'none';
                });
            }

            previous_elements_count = videoBlocks.length;
        }
    });