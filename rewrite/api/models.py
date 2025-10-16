import uuid
from django.db import models


class Community(models.Model):
    """Represents a community/organization in the system"""
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    tag = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    website = models.URLField(max_length=500, null=True, blank=True)
    image_url = models.URLField(max_length=500, null=True, blank=True)
    game_servers = models.JSONField(null=True, blank=True)
    voice_comms = models.JSONField(null=True, blank=True)
    repositories = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'communities'
        verbose_name_plural = 'communities'

    def __str__(self):
        return f"{self.name} [{self.tag}]"


class User(models.Model):
    """Represents a user in the system"""
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nickname = models.CharField(max_length=255)
    steam_id = models.CharField(max_length=255, unique=True)
    community = models.ForeignKey(
        Community,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='members'
    )
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"{self.nickname} ({self.steam_id})"


class Permission(models.Model):
    """Represents a user permission"""
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='permissions')
    permission = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'permissions'
        unique_together = [['user', 'permission']]

    def __str__(self):
        return f"{self.user.nickname}: {self.permission}"


class Mission(models.Model):
    """Represents a mission/event in the system"""
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('community', 'Community'),
        ('private', 'Private'),
        ('hidden', 'Hidden'),
    ]

    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    briefing_time = models.DateTimeField(null=True, blank=True)
    slot_list_time = models.DateTimeField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    visibility = models.CharField(max_length=50, choices=VISIBILITY_CHOICES, default='hidden')
    tech_teleport = models.BooleanField(default=False)
    tech_respawn = models.BooleanField(default=False)
    details_map = models.CharField(max_length=255, null=True, blank=True)
    details_game_mode = models.CharField(max_length=255, null=True, blank=True)
    details_required_dlcs = models.JSONField(null=True, blank=True)
    game_server = models.JSONField(null=True, blank=True)
    voice_comms = models.JSONField(null=True, blank=True)
    repositories = models.JSONField(null=True, blank=True)
    rules_of_engagement = models.TextField(blank=True, default='')
    image_url = models.URLField(max_length=500, null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='missions')
    community = models.ForeignKey(
        Community,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='missions'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'missions'

    def __str__(self):
        return self.title


class MissionSlotGroup(models.Model):
    """Represents a slot group within a mission"""
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    order_number = models.IntegerField(default=0)
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='slot_groups')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'missionSlotGroups'
        ordering = ['order_number', 'title']

    def __str__(self):
        return f"{self.mission.title}: {self.title}"


class MissionSlot(models.Model):
    """Represents a slot within a mission slot group"""
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    detailed_description = models.TextField(blank=True, default='')
    order_number = models.IntegerField(default=0)
    required_dlcs = models.JSONField(null=True, blank=True)
    slot_group = models.ForeignKey(MissionSlotGroup, on_delete=models.CASCADE, related_name='slots')
    assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_slots'
    )
    restricted_community = models.ForeignKey(
        Community,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='restricted_slots'
    )
    blocked = models.BooleanField(default=False)
    reserve = models.BooleanField(default=False)
    auto_assignable = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'missionSlots'
        ordering = ['order_number', 'title']
        unique_together = [['slot_group', 'assignee']]

    def __str__(self):
        return f"{self.slot_group.title}: {self.title}"


class MissionSlotRegistration(models.Model):
    """Represents a user's registration for a mission slot"""
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='slot_registrations')
    slot = models.ForeignKey(MissionSlot, on_delete=models.CASCADE, related_name='registrations')
    comment = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'missionSlotRegistrations'
        unique_together = [['user', 'slot']]

    def __str__(self):
        return f"{self.user.nickname} -> {self.slot.title}"


class MissionSlotTemplate(models.Model):
    """Represents a reusable slot template"""
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='slot_templates')
    community = models.ForeignKey(
        Community,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='slot_templates'
    )
    slot_groups = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'missionSlotTemplates'

    def __str__(self):
        return self.title


class MissionAccess(models.Model):
    """Represents access rights to a mission"""
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='accesses')
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='mission_accesses'
    )
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='mission_accesses'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'missionAccesses'
        unique_together = [['mission', 'user'], ['mission', 'community']]

    def __str__(self):
        target = self.user.nickname if self.user else self.community.name if self.community else 'Unknown'
        return f"{self.mission.title} -> {target}"


class CommunityApplication(models.Model):
    """Represents a user's application to join a community"""
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
    ]

    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='submitted')
    application_text = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'communityApplications'
        unique_together = [['user', 'community']]

    def __str__(self):
        return f"{self.user.nickname} -> {self.community.name} ({self.status})"


class Notification(models.Model):
    """Represents a notification for a user"""
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=255)
    title = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField()
    additional_data = models.JSONField(null=True, blank=True)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.nickname}: {self.notification_type}"

