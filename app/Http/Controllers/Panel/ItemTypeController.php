<?php

namespace App\Http\Controllers\Panel;

use App\ItemType;
use App\Jobs\Create;
use App\Jobs\Delete;
use App\Jobs\Update;
use App\Traits\ResponseManager;
use Exception;
use Illuminate\Http\Request;
use App\Http\Controllers\Controller;
use Illuminate\Http\Response;
use Illuminate\Validation\ValidationException;

class ItemTypeController extends Controller
{
    use ResponseManager;

    /**
     * Display a listing of the resource.
     *
     * @return Response
     */
    public function index()
    {
        $itemTypes = ItemType::all();
        return $this->sendData('list', $itemTypes, 200);
    }

    /**
     * Store a newly created resource in storage.
     *
     * @param Request $request
     * @return Response
     * @throws ValidationException
     */
    public function store(Request $request)
    {
        $rules = [
            'title' => 'required|string',
            'category' => 'required|string',
        ];

        $this->validate($request, $rules);
        ItemType::query()->create($request->only('title', 'category'));
        return $this->sendData('message', "ItemType is queued to be created.", 201);
    }

    /**
     * Display the specified resource.
     *
     * @param ItemType $itemType
     * @return Response
     */
    public function show(ItemType $itemType)
    {
        return $this->sendData('list', [$itemType], 200);
    }

    /**
     * Update the specified resource in storage.
     *
     * @param Request $request
     * @param ItemType $itemType
     * @return Response
     * @throws ValidationException
     */
    public function update(Request $request, ItemType $itemType)
    {
        $data = $request->all();
        $rules = [
            'title' => 'string',
            'category' => 'string',
        ];

        $this->validate($request, $rules);
        if (array_key_exists('title', $data))
            $itemType['title'] = $data['title'];
        if (array_key_exists('category', $this->data))
            $itemType['category'] = $data['category'];
        $itemType->save();
        return $this->sendData('message', "ItemType is updated.", 201);
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param ItemType $itemType
     * @return void
     * @throws Exception
     */
    public function destroy(ItemType $itemType)
    {
        $itemType->delete();
        return $this->sendData('message', 'item type is queued to be deleted', 200);
    }
}
