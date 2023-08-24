import requests
import os
import pandas as pd
import plotly.graph_objects as go
import numpy as np


class Integration:
    def __init__(self, username):
        if not isinstance(username, str):
            raise ValueError("Username must be a string")
        self.username = username
        self._bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")
        self.user_id = self._get_id_from_username()

    def _bearer_oauth(self, r, user_agent):
        """
        Method required by bearer token authentication.
        """

        r.headers["Authorization"] = f"Bearer {self._bearer_token}"
        r.headers["User-Agent"] = user_agent
        return r

    def _connect_to_endpoint(self, url, user_agent, params):
        response = requests.request(
            "GET",
            url,
            auth=lambda r: self._bearer_oauth(r, user_agent),
            params=params,
        )
        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )
        return response.json()

    def get_params(self, max_results, **kwargs):
        next_token = kwargs.get("next_token")
        if next_token:
            return {
                "max_results": max_results,
                "tweet.fields": "created_at,public_metrics",
                "pagination_token": next_token,
            }
        else:
            return {
                "max_results": max_results,
                "tweet.fields": "created_at,public_metrics",
            }

    def _get_id_from_username(self):
        url = f"https://api.twitter.com/2/users/by?usernames={self.username}"
        json_response = self._connect_to_endpoint(
            url=url, user_agent="v2UserLookupPython", params=""
        )

        # TODO: Make some kind of try-except here,
        # TODO: to check if the user actually exists

        id = json_response["data"][0]["id"]
        return id

    # TODO: Allow pagination
    def _get_user_timeline(self, max_results):
        url = f"https://api.twitter.com/2/users/{self.user_id}/tweets"
        params = self.get_params(max_results)
        json_response = self._connect_to_endpoint(
            url=url, user_agent="v2UserTweetsPython", params=params
        )

        return json_response

    def get_tweet_table(self, max_results, **kwargs):
        json_response = self._get_user_timeline(max_results=10)

        created_at = []
        text = []
        retweet_count = []
        reply_count = []
        like_count = []
        quote_count = []
        bookmark_count = []
        impression_count = []

        if isinstance(json_response, dict):
            for i in json_response["data"]:
                created_at.append(i["created_at"])
                text.append(i["text"])
                retweet_count.append(i["public_metrics"]["retweet_count"])
                reply_count.append(i["public_metrics"]["reply_count"])
                like_count.append(i["public_metrics"]["like_count"])
                quote_count.append(i["public_metrics"]["quote_count"])
                bookmark_count.append(i["public_metrics"]["bookmark_count"])
                impression_count.append(i["public_metrics"]["impression_count"])

        df = pd.DataFrame()
        df["created_at"] = created_at
        df["Publiceringsdato"] = df["created_at"].str.split("T").str[0]
        df["Tekst"] = text
        df["Retweets"] = retweet_count
        df["Replies"] = reply_count
        df["Likes"] = like_count
        df["Citeringer"] = quote_count
        df["Bogmarkeringer"] = bookmark_count
        df["Impressions"] = impression_count
        df["Popularitet"] = (
            df["Retweets"]
            + df["Replies"]
            + df["Likes"]
            + df["Citeringer"]
            + df["Bogmarkeringer"]
        )

        self.tweet_table = df
        return json_response

    def visualize_popularity(self, df):
        df["Publiceringsdato"] = df["Publiceringsdato"].astype(str)
        fig = go.Figure()

        # Original scatter plot
        fig.add_trace(
            go.Scatter(
                x=df["Publiceringsdato"],  # date/time data for the x-axis
                y=df["Popularitet"],  # polarity scores for the y-axis
                mode="markers",  # scatter plot
                name="Popularitet",  # name of the trace
                text=df.index,
                hoverinfo="text",
                marker=dict(
                    size=10,
                    color=df["Popularitet"],  # set color to polarity score
                    colorscale="RdYlGn",  # choose a colorscale
                    reversescale=False,  # reverse to have green at top
                    #                    colorbar=dict(
                    #                        title="Popularity Score",
                    #                    ),
                ),
            )
        )

        # Add a trendline
        z = np.polyfit(range(len(df["Publiceringsdato"])), df["Popularitet"], 1)
        p = np.poly1d(z)
        fig.add_trace(
            go.Scatter(
                x=df["Publiceringsdato"],
                y=p(range(len(df["Publiceringsdato"]))),
                mode="lines",
                name="Trendline",
                line=dict(color="grey"),
            )
        )

        fig.update_layout(
            title="Popularitet over tid",
            xaxis_title="Tid",
            yaxis_title="Popularitet",
            # xaxis=dict(
            #     tickmode="linear",
            #     dtick="86400000",  # One day in milliseconds
            # ),
        )

        return fig


if __name__ == "__main__":
    foo = Integration("rihanna")
    # timeline = foo._get_user_timeline(max_results=10)
    # print(timeline)
    foo.get_tweet_table(5)

    fig = foo.visualize_popularity(foo.tweet_table)

    print(type(fig))
