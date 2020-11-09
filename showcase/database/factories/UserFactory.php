<?php

/** @var \Illuminate\Database\Eloquent\Factory $factory */

use App\Item;
use App\ItemType;
use App\Kind;
use App\User;
use Illuminate\Support\Str;
use Faker\Generator as Faker;

/*
|--------------------------------------------------------------------------
| Model Factories
|--------------------------------------------------------------------------
|
| This directory should contain each of the model factory definitions for
| your application. Factories provide a convenient way to generate new
| model instances for testing / seeding your application's database.
|
*/

$factory->define(User::class, function (Faker $faker) {
    return [
        'name' => $faker->name,
        'email' => $faker->unique()->safeEmail,
        'email_verified_at' => now(),
        'password' => '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', // password
        'remember_token' => Str::random(10),
    ];
});

$factory->define(Item::class, function (Faker $faker) {
    return [
        'price' => $faker->randomFloat(2, 0, 100),
        'description' => $faker->paragraph(1),
        'kind_id' => $faker->numberBetween(1, 20),
    ];
});

$factory->define(Kind::class, function (Faker $faker) {
    return [
        'title' => $faker->word,
        'min_price' => $faker->randomFloat(2, 0, 49),
        'max_price' => $faker->randomFloat(2, 50, 100),
        'item_type_id' => $faker->numberBetween(1, 10),
    ];
});

$factory->define(ItemType::class, function (Faker $faker) {
    return [
        'title' => $faker->word,
        'category' => $faker->word,
    ];
});
