<?php

use App\Item;
use App\ItemType;
use App\Kind;
use App\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| is assigned the "api" middleware group. Enjoy building your API!
|
*/

Route::prefix('items')->group(function() {
    Route::get('', 'Panel\ItemController@index');
    Route::get('{item}', 'Panel\ItemController@show');
    Route::post('', 'Panel\ItemController@store')->middleware('auth:api');
    Route::put('{item}', 'Panel\ItemController@update')->middleware('auth:api');
    Route::delete('{item}', 'Panel\ItemController@destroy')->middleware('auth:api');
});

Route::prefix('itemTypes')->group(function() {
    Route::get('', 'Panel\ItemTypeController@index');
    Route::get('{itemType}', 'Panel\ItemTypeController@show');
    Route::post('', 'Panel\ItemTypeController@store')->middleware('auth:api');
    Route::put('{itemType}', 'Panel\ItemTypeController@update')->middleware('auth:api');
    Route::delete('{itemType}', 'Panel\ItemTypeController@destroy')->middleware('auth:api');
});

Route::prefix('kinds')->group(function() {
    Route::get('', 'Panel\KindController@index');
    Route::get('{kind}', 'Panel\KindController@show');
    Route::post('', 'Panel\KindController@store')->middleware('auth:api');
    Route::put('{kind}', 'Panel\KindController@update')->middleware('auth:api');
    Route::delete('{kind}', 'Panel\KindController@destroy')->middleware('auth:api');
});

Route::get('search', 'Panel\SearchController@search');

Route::group(['prefix' => 'auth'], function () {
    Route::post('login', 'Auth\ApiAuthController@login');
    Route::post('signup', 'Auth\ApiAuthController@signup');
    Route::get('logout', 'Auth\ApiAuthController@logout');
    Route::get('user', function (Request $request) {
        return $request->user();
    });
});

