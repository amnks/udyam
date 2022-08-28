var waypoint = new Waypoint({
    element: document.getElementById('element-waypoint'),
    handler: function(direction) {
      notify(this.element.id + ' triggers at ' + this.triggerPoint)
    },
    offset: '75%'
  })

  



  $(document).ready(function() {
    $('.progress-bar').waypoint(function() {
      $('.progress-bar').css({
        animation: "animate-positive 2s",
        opacity: "1"
      });
    }, 
      { offset: '75%' }
    );
  })