var app = angular.module('motty', ['ngResource'], function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});

// resources
app.factory('Actions', ['$resource', function($resource) {
    return $resource('/app/api/actions', null, {
        'get': {isArray:true}
    });
}]);
app.factory('Action', ['$resource', function($resource) {
    return $resource('/app/api/action/:actionId/:action', {actionId:'@id', action:'@action'}, {
        get: {method:'GET'},
        create: {method:'POST'},
        update: {method:'POST', action:'edit'},
        delete: {method:'GET', action:'delete'}
    });
}])

// controllers
app.controller('ActionList.ctrl', function($scope, Actions, Action){
    $scope.actions = [];

    Actions.get(function(res){
        $scope.actions = res;
    });
});