<?php

declare(strict_types=1);

namespace Lemon\Joe;

use Discord\Discord;
use Discord\Parts\Channel\Message;
use Discord\Parts\Permissions\ChannelPermission;
use Discord\Parts\User\Member;
use Discord\Parts\WebSockets\MessageReaction;
use Discord\WebSockets\Event as DiscordEvent;

class Events
{

    public const ROLES = [
        '1021854900310786079' => '919211156399333416',
        '1021854918107213907' => '919211274720669726', 
        '1021854984666615868' => '919211449367294002',
    ];

    #[Event(DiscordEvent::MESSAGE_CREATE)]
    public function message(Message $message, Discord $discord)
    {
        if (str_starts_with($message->content, '$')) {
            $args = explode(' ', $message->content);
            $command = trim($args[0], '$'); 

            $message->channel->sendMessage('Command '.$command.' does not exist, did you mean TODO?');
        }
    }

    #[Event(DiscordEvent::GUILD_MEMBER_ADD)]
    public function join(Member $member)
    {
        $member->addRole('924600166026186822');
    }

    #[Event(DiscordEvent::MESSAGE_REACTION_ADD)]
    public function reaction(MessageReaction $reaction)
    {
        $method = match ($reaction->channel_id) {
            '1002247733362573402' => 'tickets',

        };


        $this->$method();
    }

    public function tickets(MessageReaction $reaction, Discord $discord)
    {
        if ($reaction->emoji->id !== '1002252036311629825') {
            return;
        }

        $file = __DIR__.'/../tickets.txt';

        $tickets = (int) file_get_contents($file);        
        $reaction->guild->channels->create([
            'name' => 'ticket-'.$tickets,
            'parent_id' => '1002251863959289937',
        ])->overwrites->create([
            'deny' => new ChannelPermission($discord, [
               'read_messages' => false
            ]),
        ]);
        $tickets++;
        file_put_contents($file, $tickets);
    }

    public function roles(MessageReaction $reaction)
    {
        $role = self::ROLES[$reaction->emoji->id] ?? null;
        if (!$role) {
            return;
        }

        $reaction->member->addRole($role);
    }
}
