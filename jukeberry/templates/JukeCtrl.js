function JukeCtrl($scope,$http) {
    $scope.play = function(artist,title) {
        var data = {'artist':artist,'title':title};
        var url = '{{url_for('add')}}';
        var method = 'POST';
        $http(
            {method: method, url: url,data: JSON.stringify(data)}
        ).success(function(data, status) {
            gotPlay(data,status);
        }).error(function(data, status) {
            gotPlay(data,status);
        });
    };
    $scope.get_songs = function() {
        var url = '{{url_for('get_songlist')}}';
        var method = 'GET';
        $http(
            {method: method, url: url}
        ).success(function(data, status) {
            gotSongs(data,status);
        }).error(function(data, status) {
            gotSongs(data,status);
        });
    };
}

