<?php

declare(strict_types=1);

namespace Lemon\Joe;

use Discord\Discord;
use ReflectionMethod;

class Joe
{
    private Discord $discord;

    public function __construct(string $token)
    {
        $this->discord = new Discord([
            'token' => $token,
        ]);

        $this->bootstrapEvents();
    }

    public function run(): void
    {
        $this->discord->run();
    }

    private function bootstrapEvents(): void
    {
        $events = new Events();
        foreach (get_class_methods($events) as $method) {
            $reflection = new ReflectionMethod($events, $method);
            $attribute = $reflection->getAttributes(Event::class)[0] ?? null;
            if (!$attribute) {
                continue;
            }
            $this->discord->on($attribute->newInstance()->event, [$events, $method]);
        }
    }
}
