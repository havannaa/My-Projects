!function(e) {
    "use strict";
    var a=function() {}
    ;
    a.prototype.createLineChart=function(e, a, r, t, i, o) {
        Morris.Line( {
            element: e, data: a, xkey: r, ykeys: t, labels: i, hideHover: "auto", gridLineColor: "#eef0f2", resize: !0, lineColors: o
        }
        )
    }
    ,
    a.prototype.createAreaChart=function(e, a, r, t, i, o, n, c) {
        Morris.Area( {
            element: e, pointSize: 3, lineWidth: 2, data: t, xkey: i, ykeys: o, labels: n, resize: !0, hideHover: "auto", gridLineColor: "#eef0f2", lineColors: c, lineWidth: 0, fillOpacity: .1, xLabelMargin: 10, yLabelMargin: 10, grid: !1, axes: !1, pointSize: 0
        }
        )
    }
    ,
    a.prototype.createDonutChart=function(e, a, r) {
        Morris.Donut( {
            element: e, data: a, resize: !0, colors: r
        }
        )
    }
    ,
    a.prototype.init=function() {
        this.createLineChart("multi-line-chart", [ {
            y: "2019-04", a: 110, b: 0, c: 0
        }
        , {
            y: "2019-05", a: 150, b: 30, c: 50
        }
        , {
            y: "2019-06", a: 20, b: 50, c: 150
        }
        , {
            y: "2019-07", a: 150, b: 80, c: 40
        }
        , {
            y: "2019-08", a: 20, b: 110, c: 150
        }
        , {
            y: "2019-09", a: 50, b: 150, c: 40
        }
        , {
            y: "2019-10", a: 150, b: 170, c: 130
        }
        ], "y", ["a", "b", "c"], ["Facebook", "Twitter", "Instagram"], ["#007BFF", "#00bcd2", "#e785da"]);
        this.createAreaChart("morris-area-chart", 0, 0, [ {
            y: "2011", a: 10, b: 15
        }
        , {
            y: "2012", a: 30, b: 35
        }
        , {
            y: "2013", a: 10, b: 25
        }
        , {
            y: "2014", a: 55, b: 45
        }
        , {
            y: "2015", a: 30, b: 20
        }
        , {
            y: "2016", a: 40, b: 35
        }
        , {
            y: "2017", a: 10, b: 25
        }
        , {
            y: "2018", a: 25, b: 30
        }
        ], "y", ["a", "b"], ["Series A", "Series B"], ["#00c292", "#03a9f3"]);
        this.createDonutChart("morris-donut-chart", [ {
            label: "Facebook", value: 27
        }
        , {
            label: "Twitter", value: 50
        }
        , {
            label: "Instagram", value: 23
        }
        ], ["#40a4f1", "#5b6be8", "#c1c5e2"])
    }
    ,
    e.Dashboard=new a,
    e.Dashboard.Constructor=a
}

(window.jQuery),
function(e) {
    "use strict";
    window.jQuery.Dashboard.init()
}

();
