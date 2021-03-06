package dam.agamers.gtidic.udl.agamers.adapters;

import android.util.Log;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.core.content.ContextCompat;

import com.squareup.picasso.Picasso;

import dam.agamers.gtidic.udl.agamers.R;
import dam.agamers.gtidic.udl.agamers.models.Event;
import dam.agamers.gtidic.udl.agamers.models.EventStatus;
import dam.agamers.gtidic.udl.agamers.models.EventType;

public class EventCommonHolder {

    private static final String TAG = "EventCommonHolder";
    private TextView eventName;
    private TextView eventDescription;
    private ImageView eventPoster;
    private ImageView eventType;
    private TextView eventStatus;
    private TextView eventStatusColor;
    private TextView distanceToEvent;

    public EventCommonHolder(@NonNull View itemView) {

        eventName = itemView.findViewById(R.id.eventNameInfo);
        eventDescription = itemView.findViewById(R.id.eventDescriptionInfo);
        eventPoster = itemView.findViewById(R.id.eventPosterInfo);
        eventStatus = itemView.findViewById(R.id.jocItemName);
        eventStatusColor = itemView.findViewById(R.id.eventStatusColourInfo);
        eventType = itemView.findViewById(R.id.jocItemPoster);
        distanceToEvent = itemView.findViewById(R.id.eventDistanceToInfo);
    }

    public void bindHolder(Event e) {

        Log.d(TAG, "bindHolder() -> Event: " + e);

        this.eventName.setText(e.getName());
        this.eventDescription.setText(e.getDescription());
        this.eventStatus.setText(e.getStatus().name());

        this.eventStatusColor.setBackground(ContextCompat.getDrawable(
                this.eventStatusColor.getContext(),
                EventStatus.getColourResource(e.getStatus())));

        this.eventStatus.setText(e.getStatus().getName());
        this.eventStatus.setTextColor(ContextCompat.getColor(
                this.eventStatus.getContext(),
                EventStatus.getColourResource(e.getStatus())));

        Log.d(TAG, "onBindViewHolder() -> cEvent: " + e.getPoster_url());
        Picasso.get().load(e.getPoster_url()).into(this.eventPoster);

        this.eventType.setImageResource(EventType.getImageResource(e.getType()));
    }

}