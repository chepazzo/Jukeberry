var jukeApp = angular.module('jukeApp',[]);

jukeApp.config(['$interpolateProvider', function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
  }]);

jukeApp.controller('JukeCtrl', function ($scope,$http,$interval,$location) {
    // data
    $scope.alwayson = {
        "status":false,
        "filters":[]
    };
    $scope.tiles="#ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    $scope.songs = [];
    $scope.artists = [];
    $scope.genres = [];
    $scope.playlist = [];
    $scope.currsong = [];
    // nav
    $scope.section = "current";
    $scope.currattr = "";
    $scope.currvalue = "";
    $scope.setfv = function(f,v) {
        $scope.currattr = f;
        $scope.currvalue = v;
    };
    $scope.issection = function(sect) {
        if ($scope.section == sect) { return true; }
        return false;
    };
    $scope.setsection = function(sect) {
        $scope.section = sect;
    };
    var refresh_interval = {
        "run":10000, // check every 10s if running
        "empty":3600000 // check every 1h if not running
    };
    // Update currently playing every 10s
    var auto = undefined;
    $scope.set_refresh = function(action) {
        if (action == 'on') {
            // If already running, don't start another!
            if (angular.isDefined(auto)) { return; }
            console.log('turning on auto refresh.');
            auto = $interval(function() {
                $scope.get_alwayson();
                $scope.get_playlist();
                $scope.get_currsong();
            },10000);
        } else {
            if (angular.isDefined(auto)) {
                console.log('turning off auto refresh.');
                $interval.cancel(auto);
                auto = undefined;
            }
        }
    };
    $scope.$on('$destroy', function() { $scope.set_refresh('off'); });
    $scope.go = function(url) {
        console.log('[go] redirecting ...');
        // why doesn't $location work?
        //$location.path(url);
        //$location.replace();
        window.open(url);
    };
    $scope.set_alwayson = function(action) {
        // The problem with this is that turning the feature off
        // resets the filter to the current attr:value.
        // This means that to put it back, you have to navigate first
        //  to the right filter.
        // To fix this, I need to split this into two functions.
        var attr = $scope.currattr;
        var value = $scope.currvalue;
        var filter = {};
        var data = {
            "status":action,
            "filters":[]
        };
        $scope.alwayson = data;
        if (attr != '' && value != '') {
            filter['attr'] = attr;
            filter['value'] = value;
            data.filters.push(filter);
        }
        var url = '{{url_for('set_alwayson')}}';
        var method = 'POST';
        $http(
            {method: method, url: url,data: JSON.stringify(data)}
        ).success(function(data, status) {
            console.log(data.data);
            console.log(status);
        }).error(function(data, status) {
            console.log('ERROR');
            console.log(data);
            console.log(status);
        });
    };
    $scope.get_alwayson = function() {
        var url = '{{url_for('get_alwayson')}}';
        var method = 'GET';
        $http(
            {method: method, url: url}
        ).success(function(data, status) {
            $scope.alwayson = data.data;
            console.log(data.data);
            console.log(status);
        }).error(function(data, status) {
            console.log('ERROR');
            console.log(data);
            console.log(status);
        });
    };
    $scope.play = function(artist,title) {
        var data = {'artist':artist,'title':title};
        var url = '{{url_for('add')}}';
        var method = 'POST';
        $http(
            {method: method, url: url,data: JSON.stringify(data)}
        ).success(function(data, status) {
            console.log(data.data);
            console.log(status);
            $scope.get_playlist();
            $scope.get_currsong();
        }).error(function(data, status) {
            console.log('ERROR');
            console.log(data);
            console.log(status);
        });
    };
    $scope.play_random = function() {
        var attr = $scope.currattr;
        var value = $scope.currvalue;
        var data = {};
        if (attr != '' && value != '') {
            data[attr] = value;
        }
        var url = '{{url_for('add_random')}}';
        var method = 'POST';
        $http(
            {method: method, url: url,data: JSON.stringify(data)}
        ).success(function(data, status) {
            console.log(data.data);
            console.log(status);
            $scope.get_playlist();
            $scope.get_currsong();
        }).error(function(data, status) {
            console.log('ERROR');
            console.log(data);
            console.log(status);
        });
    };
    $scope.get_songs = function() {
        var url = '{{url_for('get_songs')}}';
        var method = 'GET';
        $http(
            {method: method, url: url}
        ).success(function(data, status) {
            $scope.songs = data.data;
            console.log(data.data);
            $scope.artists = find_attrs(data.data,'artist');
            $scope.genres = find_attrs(data.data,'genre');
        }).error(function(data, status) {
            console.log('ERROR');
            console.log(data);
            console.log(status);
        });
    };
    $scope.get_artists = function() {
        var url = '{{url_for('get_artists')}}';
        var method = 'GET';
        $http(
            {method: method, url: url}
        ).success(function(data, status) {
            $scope.artists = data.data;
            console.log(data.data);
        }).error(function(data, status) {
            console.log('ERROR');
            console.log(data);
            console.log(status);
        });
    };
    $scope.get_currsong = function() {
        var url = '{{url_for('get_currsong')}}';
        var method = 'GET';
        $http(
            {method: method, url: url}
        ).success(function(data, status) {
            $scope.currsong = data.data;
            /* in a multi-page, single-front application,
               the page will get a fresh load after adding songs
               and coming back to the main page and we know that
               there won't be any new data unless the user
               navigates off of the page and adds something anyway.
             */
            /* If this gets turned into a single-page app where the
               front-end is expected to be seen by multiple devices, then
               this should change to make the refresh interval longer when 
               nothing is currently playing instead of turning it off.
             */
            if ($scope.currsong == null) {
                $scope.set_refresh('off');
            } else {
                $scope.set_refresh('on');
            }
            console.log(data.data);
        }).error(function(data, status) {
            console.log('ERROR');
            console.log(data);
            console.log(status);
        });
    };
    $scope.get_playlist = function() {
        var url = '{{url_for('get_playlist')}}';
        var method = 'GET';
        $http(
            {method: method, url: url}
        ).success(function(data, status) {
            $scope.playlist = data.data;
            console.log(data.data);
        }).error(function(data, status) {
            console.log('ERROR');
            console.log(data);
            console.log(status);
        });
    };
    $scope.get_playlist_length = function() {
        secs = 0;
        for (i=0; i<$scope.playlist.length; i++) {
            secs += $scope.playlist[i].secs;
        }
        return secs;
    };
    $scope.get_songs_by_artist = function(artist) {
        return find_songs($scope.songs,'artist',artist);
    };
    $scope.find_songs = function(attr,value) {
        if (value == '') { return $scope.songs; }
        return find_songs($scope.songs,attr,value);
    };
    $scope.find_attrs = function(attr) {
        return find_attrs($scope.songs,attr);
    };
    $scope.get_playlist();
    $scope.get_currsong();
    $scope.get_songs();
    $scope.get_alwayson();
});

jukeApp.filter('secs2hms', function() {
  return function(secs,type) {
    var d = parseInt( secs / (60*60*24) );
    var h = parseInt( secs / (60*60) ) % 24;
    var m = parseInt( secs / 60 ) % 60;
    var s = secs % 60;
    var tstr = '';
    if (type == 'h:m:s') {
        var buff = (h > 0) ? '0' : ' ';
        tstr += (buff+m).slice(-2) + ":" + ('0'+s).slice(-2);
        if (h>0) { tstr = h + ":" + tstr; }
    } else {
        if(d > 0) tstr += d + "d ";
        if(h > 0) tstr += h + "h ";
        if(m > 0) tstr += m + "m ";
        tstr += s + "s";
    }
    return tstr;
  }
});

function find_attrs(songs,attr) {
    retobj = {};
    for (var i = 0; i < songs.length; i++) {
        val = songs[i][attr];
        if (val == null) { continue; }
        if (val == '') { continue; }
        if (typeof val == 'string') {
            retobj[val] = 1;
        } else {
            for (var j = 0; j< val.length; j++) { 
                retobj[val[j]] = 1;
            }
        }
    }
    attrs = Object.keys(retobj);
    return attrs;
    
}

function find_songs(songs,attr,value) {
    // Requires exact matches
    // This is ok because humans won't be typing.
    var retsongs = []
    for (var i = 0; i < songs.length; i++) {
        val = songs[i][attr];
        if (val == null) { continue; }
        if (val.indexOf(value) != -1) {
            retsongs.push(songs[i]);
        }
    }
    return retsongs;
}
