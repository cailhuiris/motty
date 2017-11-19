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

    $scope._dtarget = {};

    Resources.get(function(res){
        $scope.resources = res;
    });

    /* creating resource */
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

    /* modifying resource */
    $scope.prepareToModify = function($idx){
        $scope._mtarget = $scope.resources[$idx];
    }

    $scope.modify = function($idx){
        Resource.save({ id: "" }, $scope._mtarget, function(resource){
            console.log(resource);
            $scope.resources[$idx].name = resource.name;
            $scope.resources[$idx].url = resource.url;
            $scope.cancelModifying();
        });
    }

    $scope.cancelModifying = function(){
        $scope._mtarget = {};
    }

    /* about deleting */
    $scope.askDelete = function($idx){
        $scope._dtarget = $scope.resources[$idx];
    }

    $scope.yesDelete = function(){
        Resource.delete({id : $scope._dtarget.id}, function(){
            location.href = '/';
        });
    }
});