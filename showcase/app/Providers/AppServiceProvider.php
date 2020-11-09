<?php

namespace App\Providers;

use App\Item;
use App\Observers\ElasticsearchObserver;
use App\Repositories\ElasticsearchShowcaseRepository;
use App\Repositories\EloquentShowcaseRepository;
use App\Repositories\ShowcaseRepository;
use Illuminate\Support\Facades\Schema;
use Illuminate\Support\ServiceProvider;
use Laravel\Passport\Passport;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     *
     * @return void
     */
    public function register()
    {
        $this->app->bind(ShowcaseRepository::class, function () {
//            return new EloquentShowcaseRepository();
            return new ElasticsearchShowcaseRepository();
        });
    }

    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        Schema::defaultStringLength(191);
        Passport::routes();

        // This makes it easy to toggle the search feature flag
        // on and off. This is going to prove useful later on
        // when deploy the new search engine to a live app.
        if (config('services.search.enabled')) {
            Item::observe(ElasticsearchObserver::class);
        }
    }
}
