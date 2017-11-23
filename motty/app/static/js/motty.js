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
    $scope.resource_error_handler = function(errors){
        if(errors.data.name) {
            toast(errors.data.name[0]);
            $('.new-resource-input').focus();
            return;
        }

        if(errors.data.url) {
            toast(errors.data.url[0]);
            $('.new-url-input').focus();
            return;
        }
    };

    $scope.saveNewResource = function() {
        Resource.save($scope.newResource, function(resource){
            $scope.resources.push(resource);
            $scope.cancelCreating();
        }, $scope.resource_error_handler);
    }

    $scope.createResource = function() {
        $scope.is_creating_resource = true;
        $("body, html").animate({
            scrollTop: $(document).height()
        }, 400)        
    }

    $scope.cancelCreating = function() {
        $scope.is_creating_resource = false;
        $scope.newResource = { name: "", url: "" }
        $('.toast').remove();
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
        }, $scope.resource_error_handler);
    }

    $scope.cancelModifying = function(){
        $scope._mtarget = {};
        $('.toast').remove();
    }

    /* about deleting */
    $scope.askDelete = function($idx){
        $scope._dtarget = $scope.resources[$idx];
    }
});

app.controller('EditActionForm.ctrl', function($scope){
    var flask = new CodeFlask;
    $scope.contentTypes = [
        { value: 'plain/text', name:'Text' },
        { value: 'application/json', name:'JSON (application/json)' },
        { value: 'application/javascript', name:'Javascript (application/javascript)' },
        { value: 'application/xml', name:'XML (application/xml)' },
        { value: 'text/xml', name:'XML (text/xml)' },
        { value: 'text/html', name:'HTML (text/html)' },
    ];

    $scope.contentType = '';

    $scope.changeContentType = function(){
        if($scope.contentType == 'application/json' || $scope.contentType == 'application/javascript') {
            flask.run('#response', {
                language: 'javascript'
            });
        } else if($scope.contentType == 'application/xml' 
           || $scope.contentType == 'text/xml'
           || $scope.contentType == 'text/html') {
            flask.run('#response', {
                language: 'html'
            });
        } else {
            flask.run('#response', {
                language: 'text'
            });
        }

        var body = $("input[name=body]").val()
        if(body != '')
            flask.update(body)
        else
            flask.update('Type response here.');

        flask.onUpdate(function(code){
            $("input[name=body]").val(code);
        });
    }

    $scope.changeContentType();
});

app.controller('ActionView.ctrl', function($scope, Action){
    
});