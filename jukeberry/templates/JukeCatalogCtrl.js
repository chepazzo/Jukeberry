var jukeApp = angular.module('jukeApp',[]);

jukeApp.config(['$interpolateProvider', function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
  }]);

jukeApp.controller('JukeCatalogCtrl', function ($scope,$http,$interval,$location) {
    // nav
    $scope.$on('$destroy', function() { $scope.set_refresh('off'); });
    $scope.go = function(url) {
        console.log('[go] redirecting ...');
        // why doesn't $location work?
        //$location.path(url);
        //$location.replace();
        window.open(url);
    };
    $scope.load_catalog = function() {
        var url = '{{url_for('load_catalog')}}';
        var method = 'GET';
        $http(
            {method: method, url: url}
        ).success(function(data, status) {
            console.log(data.data);
        }).error(function(data, status) {
            console.log('ERROR');
            console.log(data);
            console.log(status);
        });
        $scope.go("/");
        //$location.path( "/index.html" );
    };
    //$scope.load_catalog();
});

