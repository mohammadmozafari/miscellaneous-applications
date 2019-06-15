<?php

namespace App;

use Illuminate\Database\Eloquent\Model;
use App\Traits\Searchable;

class Item extends Model
{
    use Searchable;

    protected $fillable = [
        'price',
        'description',
        'kind_id'
    ];

    public function kind()
    {
        return $this->belongsTo(Kind::class);
    }
}
