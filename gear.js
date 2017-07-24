function mkgear(element, num_of_trajs=5, spiral_step=1, gear_r=0.5) {
    var state = 1;
    var s = state;

    /* 
       FROM: https://github.com/liabru/gears-d3-js/blob/master/gears.d3.js
       SEEALSO: http://brm.io/gears-d3-js/
       LICENSE: MIT
       */

    function gear_paths(options) {
        var addendum = options.addendum || 8,
            dedendum = options.dedendum || 3,
            thickness = options.thickness || 0.7,
            profileSlope = options.profileSlope || 0.5,
            holeRadius = options.holeRadius || 5,
            teeth = Math.round(options.teeth) || 16,
            radius = options.radius - addendum,
            rootRadius = radius - dedendum,
            outsideRadius = radius + addendum,
            circularPitch = (1 - thickness) * 2 * Math.PI / teeth,
            pitchAngle = thickness * 2 * Math.PI / teeth,
            slopeAngle = pitchAngle * profileSlope * 0.5,
            addendumAngle = pitchAngle * (1 - profileSlope),
            theta = (addendumAngle * 0.5 + slopeAngle),
            path = ['M', rootRadius * Math.cos(theta), ',', 
                rootRadius * Math.sin(theta)];

        for(var i = 0; i < teeth; i++) {
            theta += circularPitch;

            path.push(
                      'A', rootRadius, ',', rootRadius, ' 0 0,1 ', 
                      rootRadius * Math.cos(theta), ',', rootRadius * Math.sin(theta),
                      'L', radius * Math.cos(theta), ',', radius * Math.sin(theta)
            );

            theta += slopeAngle;
            path.push(
                      'L', outsideRadius * Math.cos(theta), ',', 
                      outsideRadius * Math.sin(theta));
            theta += addendumAngle;
            path.push(
                      'A', outsideRadius, ',', outsideRadius, ' 0 0,1 ', 
                      outsideRadius * Math.cos(theta), ',', 
                      outsideRadius * Math.sin(theta));

            theta += slopeAngle;

            path.push(
                      'L', radius * Math.cos(theta), ',', 
                      radius * Math.sin(theta),
                      'L', rootRadius * Math.cos(theta), ',', rootRadius * Math.sin(theta)
            );
        }

        function circle(radius, swap_flag) {
            return ['M0,', -radius, 'A', radius, ',', radius, 
                ' 0 0,' + swap_flag + ' 0,', radius, 'A', radius, 
                ',', radius, ' 0 0,' + swap_flag + ' 0,', -radius, 'Z']
        }

        Array.prototype.push.apply(path, circle(holeRadius, '0'));
        var ring_path  = circle(outsideRadius, '1')
            .concat(circle(holeRadius, '0'))
        return {gear: path.join(''), 'ring': ring_path.join('')};
    }

    /* END FROM */

    function gear_path(options) {
        return gear_paths(options).gear
    }

    function gear_ring_path(options) {
        return gear_paths(options).ring
    }

    function theta0(n) {
        return n * 2 * Math.PI / num_of_trajs;
    }

    function points(n) {
        return d3.range(0, 20 * Math.PI, 0.1).map(function(t) {
            return {
                theta: s * t + theta0(n), 
                r: Math.exp(-t / spiral_step), 
            };
        });
    }

    function mktraj() {
        var traj = d3.range(num_of_trajs).map(function(n) {
            return points(n);
        });
        return traj;
    }

    var width = 450,
        height = 450,
        radius = Math.min(width, height) / 2;

    var r = d3.scaleLinear()
        .domain([0, 1])
        .range([0, radius]);

    var svg = d3.select(element)
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", "translate(" + 
              width / 2 + "," + height / 2 + ")");
    var line = d3.radialLine()
        .radius(function(d) { return r(d.r); })
        .angle(function(d) {
            return -d.theta + Math.PI / 2; });

    function gear_rotate(d) {
        return 'rotate(' + d.angle * (180 / Math.PI) + ')';
    }

    function gear_angle() {
        return s * Math.log(gear_r) * spiral_step;
    }

    function gear_data() {
        return [{radius: r(gear_r),
            holeRadius: r(gear_r-0.06),
            addendum: 4,
            dedendum: 3,
            thickness: 0.6,
            teeth: Math.round(10 + gear_r * 30),
            profileSlope: 0.7,
            angle: gear_angle()}];
    }

    function clamp(n, min, max) {
        return Math.min(Math.max(n, min), max);
    };

    function dragstarted(d) {
        d3.select(this).raise().classed("dragging", true);
        delta_r = gear_r - r.invert(Math.sqrt(Math.pow(d3.event.x, 2) + 
            Math.pow(d3.event.y, 2)))
    }

    function dragged(d) {
        gear_r = clamp(delta_r + 
                       r.invert(Math.sqrt(Math.pow(d3.event.x, 2) + 
                                          Math.pow(d3.event.y, 2))), 
            0.08, 1);
        Object.assign(d, gear_data()[0])
        update()
    }

    function dragended(d) {
        d3.select(this).classed("dragging", false);
    }

    function update(first) {
        var trajs = svg.selectAll(".line")
            .data(mktraj());
        trajs.enter().append("path").attr("class", "line")
            .merge(trajs)
            .attr("d", line)

        var gear = svg.selectAll(".gear")
            .data(gear_data());
        gear.enter().append("path").attr("class", "gear")
            .merge(gear)
            .attr("d", gear_path)
            .attr("transform", gear_rotate);

        var gear_ring = svg.selectAll('.gear_ring')
            .data(gear_data());
        gear_ring = gear_ring.enter()
            .append("path").attr("class", "gear_ring")
            .merge(gear_ring).attr("d", gear_ring_path);
        if (first) {
            gear_ring.call(d3.drag()
                           .on("start", dragstarted)
                           .on("drag", dragged)
                           .on("end", dragended));
        }
    }

    function do_transition() {
        var duration = 2000;
        var ease = d3.easeCubic;
        d3.select(element).on("click", null);
        var newstate = 1 - state;
        timer = d3.timer(function (elapsed) {
            // compute how far through the animation we are (0 to 1)
            var t = Math.min(1, ease(elapsed / duration));
            s = t * newstate + (1-t)*state
            update()
            if (t === 1) {
                // stop this timer since we are done animating.
                state = newstate;
                timer.stop();
                d3.select(element).on("click", do_transition);
            }
        });
    }

    update(true);
    /*
    svg.append('circle')
        .attr('cx', 0)
        .attr('cy', 0)
        .attr('r', 5)
        .attr("class", "singpoint");
    */
    d3.select(element).on("click", do_transition);
};
