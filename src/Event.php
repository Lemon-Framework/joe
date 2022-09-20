<?php

declare(strict_types=1);

namespace Lemon\Joe;

use Attribute;

#[Attribute(Attribute::TARGET_METHOD)]
class Event
{
    public function __construct(
        public readonly string $event
    ) {

    }
}
