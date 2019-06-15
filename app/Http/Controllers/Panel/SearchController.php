<?php

namespace App\Http\Controllers\Panel;

use App\Http\Controllers\Controller;
use App\Repositories\ShowcaseRepository;
use App\Traits\ResponseManager;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Log;
use Memcached;

class SearchController extends Controller
{
    use ResponseManager;

    /**
     * @param ShowcaseRepository $repo
     * @param Request $request
     * @return \Illuminate\Http\JsonResponse
     * @throws \Illuminate\Validation\ValidationException
     */
    public function search(ShowcaseRepository $repo, Request $request)
    {
        // validate that a page number is sent in the request
        $rules = [
            'page' => 'required'
        ];
        $this->validate($request, $rules);


        // hash search query with no salt
        $searchQuery =
            hash('sha256',
            json_encode(request()->only(['price', 'description', 'kindTitle', 'typeTitle', 'category', 'page'])));

        $num = request()->page;

        $results = Cache::get($searchQuery);
        if (!$results)
        {
            $results = $repo->search(request()->except('page'), $num);
            Cache::put($searchQuery, json_encode($results), 600);
        }
        else
        {
            $results = json_decode($results);
        }
        return $this->sendData("search-result", $results, 200);
    }
}
