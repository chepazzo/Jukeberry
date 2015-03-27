var jukeApp = angular.module('jukeApp',[]);

jukeApp.config(['$interpolateProvider', function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
  }]);

jukeApp.controller('JukeCtrl', function ($scope,$rootScope,$http) {
    $scope.artists = [];
    $scope.songs = [];
    $scope.play = function(artist,title) {
        var data = {'artist':artist,'title':title};
        var url = '{{url_for('add')}}';
        var method = 'POST';
        $http(
            {method: method, url: url,data: JSON.stringify(data)}
        ).success(function(data, status) {
            gotPlay(data.data,status);
        }).error(function(data, status) {
            gotPlay(data.data,status);
        });
    };
    $scope.get_songs = function() {
        var url = '{{url_for('get_songlist')}}';
        var method = 'GET';
        $http(
            {method: method, url: url}
        ).success(function(data, status) {
            $scope.songs = data.data;
            console.log(data.data);
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
            //gotSongs(data.data,status);
            $scope.artists = data.data;
            console.log(data.data);
        }).error(function(data, status) {
            console.log('ERROR');
            console.log(data);
            console.log(status);
        });
    };
    $scope.get_artists();
    $scope.get_songs();
});

