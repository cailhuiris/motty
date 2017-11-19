var app = angular.module('motty', ['ngResource', 'ngDialog'], function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});

// resources
app.factory('Resources', ['$resource', function($resource){
    return $resource('/motty/api/resources', null, {
        'get': { isArray:true }
    })
}]);

app.factory('Resource', ['$resource', function($resource){
    return $resource('/motty/api/resource/:id/:action', {id:'@id', action:'@action'}, {
        save: { method: 'POST' },
        delete: { method: 'GET', params: { action:'delete' } }
    });
}]);

app.factory('Action', ['$resource', function($resource) {
    return $resource('/motty/api/action/:id/:action', {id:'@id', action:'@action'}, {
        get: { method: 'GET' },
        save: { method: 'POST' },
        delete: { method: 'GET', params: { action:'delete' } },
        deleteAll: { method: 'POST', params: { id: 'delete', action: 'all' } }
    });
}])

// controllers
app.controller('ResourceList.ctrl', function($scope, Resources, Resource){
    $scope.is_creating_resource = false;
    $scope.newResource = { name: "", url: "" }
    $scope.resources = [];

    $scope.targetResource = {};

    Resources.get(function(res){
        $scope.resources = res;
    });

    $scope.saveNewResource = function() {
        Resource.save($scope.newResource, function(resource){
            $scope.resources.push(resource);
            $scope.cancelCreating();
        });
    }

    $scope.createResource = function() {
        $scope.is_creating_resource = true;
    }

    $scope.cancelCreating = function() {
        $scope.is_creating_resource = false;
        $scope.newResource = { name: "", url: "" }
    }

    $scope.askDelete = function($idx){
        $scope.targetResource = $scope.resources[$idx];
    }

    $scope.yesDelete = function(){
        Resource.delete({id : $scope.targetResource.id}, function(){
            location.href = '/';
        });
    }
});